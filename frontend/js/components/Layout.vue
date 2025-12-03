<script setup lang="ts">
import { Link, usePage } from '@inertiajs/vue3';
import IntegracarLogo from './IntegracarLogo.vue';
import { Conversa, Usuario } from '@/types/index';

const page = usePage<{
    urls: Record<string, string>,
    user: Usuario,
    conversas: Conversa[],
}>();
</script>

<template>
    <div class="drawer lg:drawer-open">
        <input id="sidebar" type="checkbox" class="drawer-toggle" checked />
        <div class="drawer-content flex flex-col min-h-screen">
            <!-- Navbar -->
            <nav
                class="navbar w-full sticky top-0 z-20 bg-linear-to-r/shorter  from-neutral to-base-300 text-secondary-content">
                <label for="sidebar" aria-label="open sidebar" class="btn btn-square btn-ghost">
                    <i class="bi bi-layout-sidebar text-xl"></i>
                </label>
                <div class="px-4">
                    <Link :href="page.props.urls['index']" class="flex items-center gap-2">
                    <IntegracarLogo />
                    Chatbot IntegraCAR
                    </Link>
                </div>
            </nav>

            <!-- Page content here -->
            <div class="grow flex flex-col">

                <slot></slot>
            </div>
        </div>

        <div class="drawer-side is-drawer-close:overflow-visible z-50">
            <label for="sidebar" aria-label="close sidebar" class="drawer-overlay"></label>
            <div
                class="flex min-h-full flex-col items-start justify-between is-drawer-close:w-14 is-drawer-open:w-64 bg-neutral text-neutral-content">
                <!-- Sidebar content here -->
                <ul class="menu w-full grow">
                    <div class="h-14"></div>
                    <li>
                        <Link :href="page.props.urls['index']"
                            class="is-drawer-close:tooltip is-drawer-close:tooltip-right" data-tip="Nova Conversa">
                        <i class="bi bi-pencil-square"></i>
                        <span class="is-drawer-close:hidden">Nova Conversa</span>
                        </Link>
                    </li>
                    <li>
                        <Link :href="page.props.urls['documentos']"
                            class="is-drawer-close:tooltip is-drawer-close:tooltip-right" data-tip="Documentos">
                        <i class="bi bi-file-earmark-text"></i>
                        <span class="is-drawer-close:hidden">Documentos</span>
                        </Link>
                    </li>
                    <li>
                        <Link :href="page.props.urls['curadoria']"
                            class="is-drawer-close:tooltip is-drawer-close:tooltip-right" data-tip="Curadoria">
                        <i class="bi bi-robot"></i>
                        <span class="is-drawer-close:hidden">Curadoria</span>
                        </Link>
                    </li>
                    <hr class="my-2">
                    <li v-for="conversa in page.props.conversas" :key="conversa.id">
                        <Link :href="page.props.urls['conversa'].replace('%(id_conversa)s', conversa.id.toString())" class="is-drawer-close:hidden">
                        <span>{{ conversa.nome }}</span>
                        </Link>
                    </li>

                </ul>
                <ul class="menu w-full">
                    <li>
                        <div class="dropdown dropdown-top  is-drawer-close:dropdown-start dropdown-center p-0 is-drawer-close:tooltip is-drawer-close:tooltip-right"
                            role="button">
                            <div tabindex="0" role="button" class="btn btn-accent w-full">
                                <i class="bi bi-person-circle"></i>
                                <span class="is-drawer-close:hidden">{{ page.props.user.name }}</span>
                            </div>
                            <ul tabindex="-1"
                                class="dropdown-content menu bg-base-300 text-base-content rounded-box z-1 w-60 p-2 shadow-sm ">
                                <li>
                                    <Link :href="page.props.urls['sair']" method="post">
                                    <i class="bi bi-box-arrow-right text-error"> </i>
                                    Sair
                                    </Link>
                                </li>
                            </ul>
                        </div>
                    </li>
                </ul>

            </div>
        </div>
    </div>
</template>
