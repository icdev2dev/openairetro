<script>
    import { onMount } from 'svelte';
    import { fetchAllData } from './dataservices';

    onMount(() => {
        fetchAllData();
        
    });
</script>
