<script>

    import { activeAssistants } from "./dataservices"; 
    import { currentModels } from "./dataservices"; 

    import { selectedAssistant } from "../stores/selectedAssistant";
    import {selectedModel} from "../stores/selectedModel"

    $: assistants = $activeAssistants 
    $: models = $currentModels

</script>



<div class="container grid">
    <div class="item">

        <div>
            Assistant
        </div>

        <div>
            <select bind:value={$selectedAssistant} >
                {#each assistants as assistant}
                    <option value={assistant.assistant_id}>
                        {assistant.assistant_name}
                    </option>
                {/each}
            </select>
        
        </div>
    </div>
    <div class="item">
        <div>
            Model
        </div>


        <div>
            <select bind:value={$selectedModel} >
                {#each models as model}
                    <option value={model}>
                        {model}
                    </option>
                {/each}
            </select>
        
        </div>


    </div>

</div>    

<style>
    
    
    
    .grid {
      display: grid;
      grid-template-columns: 1fr 1fr; /* 20% and 80% */
      gap: 10px;
    }
</style>

