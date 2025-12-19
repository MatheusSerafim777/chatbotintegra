<script setup lang="ts">
import { ref, nextTick, computed, watch, onMounted } from 'vue';
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
const editable = ref<HTMLElement | null>(null);
const containerMensagens = ref<HTMLElement | null>(null);
const mensagemRef = ref<typeof Mensagem | null>(null);

const mensagensRaiz = computed<number[]>(
    () =>
        Object.values(mapMensagens.value)
            .filter(mensagem => mensagem.mensagem_pai === null)
            .map(mensagem => mensagem.id!)
);

watch(
    idConversa, (novoIdConversa, antigoIdConversa) => {
        console.log(page.props)
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
    if (!pergunta.value.trim()) return;

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

    const response = await fetch('/api/chat', {
        method: 'POST',
        body: JSON.stringify(payload),
    });

    if (!response.body) {
        return;
    }
    // faça uma tabela simples, sem `
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
        mapMensagens.value[idMensagemBot].conteudo += decoder.decode(value);  // input de escrita
        scrollParaUltimaMensagem();
    };
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
})
</script>

<template>
    <div class="flex-1 pb-4 mx-auto flex flex-col justify-between w-full">
        <div class="overflow-auto flex-1 max-h-[85vh]" ref="containerMensagens">
            <div class="w-full max-w-3xl mx-auto py-2">
                <Mensagem ref="mensagemRef" v-if="mensagensRaiz.length > 0" :map-mensagens="mapMensagens"
                    :ids="mensagensRaiz" />
            </div>
        </div>
        <form @submit.prevent="enviarMensagem" class="w-full max-w-3xl mx-auto">
            <label for="pergunta"
                class="relative flex justify-between items-center gap-4 min-h-14 rounded-[28px] bg-base-300 text-base-content shadow-2xl shadow-base-300 p-2.5 cursor-text"
                @click="editable?.focus()">

                <!-- placeholder -->
                <span v-if="!pergunta.trim()"
                    class="absolute left-2.5 top-1/2 -translate-y-1/2 text-base-content/50 pointer-events-none select-none">
                    Digite sua mensagem...
                </span>
                <div class="w-full max-h-60 overflow-scroll">
                    <div ref="editable" autofocus="true" id="pergunta" contenteditable="true" role="textbox"
                        aria-multiline="true"
                        class="w-full bg-transparent focus:outline-none p-0 font-medium min-h-6 whitespace-pre-wrap wrap-break-word"
                        @input="pergunta = editable?.innerText ?? ''"
                        @keydown="if ($event.key === 'Enter') { if (!$event.shiftKey) { $event.preventDefault(); enviarMensagem(); } }"
                        @paste="handlePaste">
                    </div>
                </div>

                <button class="btn btn-neutral text-neutral-content h-9 w-9 btn-circle p-0"
                    :disabled="!pergunta.trim()">
                    <i class="bi bi-arrow-up-short text-4xl h-9 w-9"></i>
                </button>
            </label>
        </form>

    </div>
</template>