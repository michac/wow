<script>
  import { store } from "./lib/store.svelte.js";
  import Drill from "./lib/components/Drill.svelte";
  import Archetype from "./lib/components/Archetype.svelte";
</script>

<main class="flex min-h-dvh items-center justify-center p-0 sm:p-6 md:p-10">
  {#if store.settings.mode === "archetypes"}
    <Archetype />
  {:else}
    <Drill />
  {/if}
</main>
