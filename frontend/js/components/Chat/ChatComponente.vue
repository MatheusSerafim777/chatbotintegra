<script setup lang="ts">
import { ref, nextTick, computed, watch, onMounted, onUnmounted } from 'vue';
import { router, usePage } from '@inertiajs/vue3';
import Mensagem from './Mensagem.vue';
import { Usuario } from '@/types/index';

export type TMensagem = {
    id: number;
    tipo: 'USUARIO' | 'ASSISTENTE';
    conteudo: string;
    mensagem_pai: number | null;
    mensagens_filhas: number[];
    curtido: boolean | null;
}

export type MapMensagens = {
    [key: number]: TMensagem;
}

type chatResponse = {
    id_conversa: number;
    id_mensagem_pergunta: number;
    id_mensagem_resposta: number;
}

const page = usePage<{
    map_mensagens: MapMensagens,
    id_conversa: number,
    user: Usuario | null,
}>();

const mapMensagens = ref<MapMensagens>(page.props.map_mensagens ?? {});

const idConversa = ref<number | null>(page.props.id_conversa ?? null);
const pergunta = ref('');
const enviandoMensagem = ref(false);
const editable = ref<HTMLElement | null>(null);
const containerMensagens = ref<HTMLElement | null>(null);
const mensagemRef = ref<typeof Mensagem | null>(null);

function focarInputMensagem(cursorNoFinal = true) {
    if (!editable.value) return;

    editable.value.focus();
    if (!cursorNoFinal) return;

    const selection = window.getSelection();
    if (!selection) return;

    const range = document.createRange();
    range.selectNodeContents(editable.value);
    range.collapse(false);
    selection.removeAllRanges();
    selection.addRange(range);
}

const handleWindowFocus = () => {
    focarInputMensagem();
};

const mensagensRaiz = computed<number[]>(
    () =>
        Object.values(mapMensagens.value)
            .filter(mensagem => mensagem.mensagem_pai === null)
            .map(mensagem => mensagem.id!)
);

watch(
    idConversa, (novoIdConversa, antigoIdConversa) => {
        if (novoIdConversa !== antigoIdConversa) {
            if (novoIdConversa == null) {
                router.visit('/', { replace: true, preserveState: true });
            } else if (page.props.user) {
                router.visit(`/c/${novoIdConversa}/`, { replace: true, preserveState: true });
            }
        }
    }
)

async function adicionarMensagem(mensagem: TMensagem) {
    mapMensagens.value[mensagem.id] = mensagem;
    await nextTick();
    scrollParaUltimaMensagem();
}

const enviarMensagem = async () => {
    if (!pergunta.value.trim() || enviandoMensagem.value) return;

    enviandoMensagem.value = true;
    const mensagemPaiSelecionada: number | null = mensagensRaiz.value.length > 0 ? mensagemRef.value?.obterIdUltimaMensagem() : null;
    const mensagemUsuario: TMensagem = {
        id: Date.now() + Math.random(),
        tipo: 'USUARIO',
        conteudo: pergunta.value,
        mensagem_pai: mensagemPaiSelecionada,
        mensagens_filhas: [],
        curtido: null,
    };
    if (mensagemPaiSelecionada !== null) {
        mapMensagens.value[mensagemPaiSelecionada].mensagens_filhas.push(mensagemUsuario.id);
    }
    await adicionarMensagem(mensagemUsuario);


    const lastUserMessage = pergunta.value;
    pergunta.value = '';
    if (editable.value) {
        editable.value.textContent = '';
    }
    await nextTick();
    focarInputMensagem(false);

    // mensagem vazia do bot
    const botMessage: TMensagem = {
        id: Date.now() + Math.random(),
        tipo: 'ASSISTENTE',
        conteudo: '',
        mensagem_pai: mensagemUsuario.id,
        mensagens_filhas: [],
        curtido: null,
    };
    mapMensagens.value[mensagemUsuario.id].mensagens_filhas.push(botMessage.id);
    await adicionarMensagem(botMessage);

    // Agora começa o streaming
    const payload = {
        mensagem: lastUserMessage,
        stream: true,
        id_mensagem_pai: mensagemPaiSelecionada,
        id_conversa: idConversa.value,
    };

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
        });

        if (!response.body) {
            mapMensagens.value[botMessage.id].conteudo = 'Não foi possível obter resposta do assistente.';
            return;
        }
        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        let primeiro = true;
        let idMensagemBot = botMessage.id;
        while (true) {
            const { value, done } = await reader.read();

            if (done) break;
            if (primeiro) {
                primeiro = false;
                const dados: chatResponse = JSON.parse(decoder.decode(value));
                idConversa.value = dados.id_conversa;

                // Atualiza o ID da mensagem do usuário
                const idAntigoUsuario = mensagemUsuario.id;
                const novoIdUsuario = dados.id_mensagem_pergunta;
                mensagemUsuario.id = novoIdUsuario;
                delete mapMensagens.value[idAntigoUsuario];
                mapMensagens.value[novoIdUsuario] = mensagemUsuario;

                // Atualiza a referência na mensagem pai
                if (mensagemPaiSelecionada !== null) {
                    const filhas = mapMensagens.value[mensagemPaiSelecionada].mensagens_filhas;
                    const index = filhas.indexOf(idAntigoUsuario);
                    if (index !== -1) {
                        filhas[index] = novoIdUsuario;
                    }
                }

                // Atualiza o ID da mensagem do bot
                const idAntigoBot = botMessage.id;
                const novoIdBot = dados.id_mensagem_resposta;
                botMessage.id = novoIdBot;
                botMessage.mensagem_pai = novoIdUsuario;
                delete mapMensagens.value[idAntigoBot];
                mapMensagens.value[novoIdBot] = botMessage;
                idMensagemBot = novoIdBot;

                // Atualiza a referência na mensagem do usuário
                const filhasUsuario = mapMensagens.value[novoIdUsuario].mensagens_filhas;
                const indexBot = filhasUsuario.indexOf(idAntigoBot);
                if (indexBot !== -1) {
                    filhasUsuario[indexBot] = novoIdBot;
                }

                continue;
            }
            mapMensagens.value[idMensagemBot].conteudo += decoder.decode(value);
            scrollParaUltimaMensagem();
        }
    } catch (error) {
        botMessage.conteudo = 'Ocorreu um erro ao enviar sua mensagem. Tente novamente.';
    } finally {
        enviandoMensagem.value = false;
        await nextTick();
        focarInputMensagem();
    }
}


function handlePaste(e: ClipboardEvent) {
    e.preventDefault()
    const text = e.clipboardData?.getData('text/plain') || ''
    document.execCommand('insertText', false, text)
}

function scrollParaUltimaMensagem(smooth = true) {
    const div = containerMensagens.value
    if (div) {
        div.scrollTo({
            top: div.scrollHeight,
            behavior: smooth ? 'smooth' : 'auto',
        })
    }
}

onMounted(async () => {
    await nextTick();
    scrollParaUltimaMensagem(false);
    focarInputMensagem();

    window.addEventListener('focus', handleWindowFocus);
});

onUnmounted(() => {
    window.removeEventListener('focus', handleWindowFocus);
});
</script>

<template>
    <div class="mx-auto flex h-full w-full max-w-5xl flex-1 flex-col justify-between gap-3 pb-2 pt-3 sm:gap-4 sm:pb-4">
        <div class="min-h-0 flex-1 overflow-y-auto px-1" ref="containerMensagens">
            <div class="mx-auto w-full max-w-3xl space-y-3 pb-1">
                <Mensagem ref="mensagemRef" v-if="mensagensRaiz.length > 0" :map-mensagens="mapMensagens"
                    :ids="mensagensRaiz" />
            </div>
        </div>
        <form @submit.prevent="enviarMensagem" class="mx-auto w-full max-w-3xl px-1">
            <label for="pergunta"
                class="relative flex min-h-14 cursor-text items-center justify-between gap-2 rounded-[28px] border border-base-content/10 bg-base-300 px-3 py-2 text-base-content shadow-lg"
                @click="editable?.focus()">

                <!-- placeholder -->
                <span v-if="!pergunta.trim()"
                    class="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 select-none text-base-content/50">
                    Digite sua mensagem...
                </span>
                <div class="flex w-full max-h-52 items-center overflow-y-auto">
                    <div ref="editable" autofocus="true" id="pergunta" contenteditable="true" role="textbox"
                        aria-multiline="true"
                        class="min-h-6 w-full wrap-break-word bg-transparent py-1 px-1 font-medium whitespace-pre-wrap focus:outline-none"
                        @input="pergunta = editable?.innerText ?? ''"
                        @keydown="if ($event.key === 'Enter') { if (!$event.shiftKey) { $event.preventDefault(); enviarMensagem(); } }"
                        @paste="handlePaste">
                    </div>
                </div>

                <button class="btn btn-neutral text-neutral-content h-9 w-9 btn-circle p-0"
                    :disabled="!pergunta.trim() || enviandoMensagem">
                    <i class="bi bi-arrow-up-short text-4xl h-9 w-9"></i>
                </button>
            </label>
        </form>

    </div>
</template>