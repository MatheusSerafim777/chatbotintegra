<script setup lang="ts">
import { Link } from '@inertiajs/vue3';
import IntegracarLogo from './IntegracarLogo.vue';
</script>

<template>
    <div class="drawer lg:drawer-open">
        <input id="sidebar" type="checkbox" class="drawer-toggle" checked />
        <div class="drawer-content flex flex-col min-h-screen">
            <!-- Navbar -->
            <nav class="navbar w-full sticky top-0 z-20 bg-neutral text-neutral-content">
                <label for="sidebar" aria-label="open sidebar" class="btn btn-square btn-ghost">
                    <i class="bi bi-layout-sidebar text-xl"></i>
                </label>
                <div class="px-4">
                    <Link href="/" class="flex items-center gap-2">
                    <IntegracarLogo /> Chatbot IntegraCAR </Link>
                </div>
            </nav>

            <!-- Page content here -->
            <div class="grow">

                <slot></slot>
            </div>
        </div>

        <div class="drawer-side is-drawer-close:overflow-visible z-50">
            <label for="sidebar" aria-label="close sidebar" class="drawer-overlay"></label>
            <div
                class="flex min-h-full flex-col items-start justify-between is-drawer-close:w-14 is-drawer-open:w-64 bg-neutral text-neutral-content">
                <!-- Sidebar content here -->
                <ul class="menu w-full grow">
                    <!-- List item -->
                    <li>
                        <button class="is-drawer-close:tooltip is-drawer-close:tooltip-right" data-tip="Homepage">
                            <i class="bi bi-house-door"></i>
                            <span class="is-drawer-close:hidden">Home
                            </span>
                        </button>
                    </li>

                    <!-- List item -->
                    <li>
                        <button class="is-drawer-close:tooltip is-drawer-close:tooltip-right" data-tip="Settings">
                            <i class="bi bi-gear"></i>
                            <span class="is-drawer-close:hidden">Configurações</span>
                        </button>
                    </li>
                </ul>
                <ul class="menu w-full">
                    <li>
                        <div class="dropdown dropdown-top  is-drawer-close:dropdown-start dropdown-center p-0 is-drawer-close:tooltip is-drawer-close:tooltip-right"
                             role="button">
                            <div tabindex="0" role="button" class="btn btn-accent w-full">
                                <i class="bi bi-person-circle"></i>
                                <span class="is-drawer-close:hidden">Lucas Zanotelli</span>
                            </div>
                            <ul tabindex="-1"
                                class="dropdown-content menu bg-base-300 text-base-content rounded-box z-1 w-52 p-2 shadow-sm ">
                                <li>
                                    <Link href="/contas/sair/" method="post">
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
