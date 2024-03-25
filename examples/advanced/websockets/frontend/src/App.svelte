<script >


import DataServices from "./components/DataServices.svelte";
import { Route, Router, Link } from "svelte-routing";

import HomePage from "./lib/pages/Home.svelte";
import AssistantsPage from "./lib/pages/Assistants.svelte";
import ThreadsPage from "./lib/pages/Threads.svelte";
import StreamPage from "./lib/pages/Stream.svelte";
import MultipleProvidersPage from "./lib/pages/MultipleProviders.svelte";

let tabs = [
    {name:'Home', route: '/', component: HomePage},
    {name:'Assistants', route: '/assistants', component: AssistantsPage},
    {name:'Threads', route: '/threads', component: ThreadsPage},
    {name:'Multiple Providers', route: '/multipleproviders', component: MultipleProvidersPage},
    {name:'Streaming', route: '/streaming/*', component: StreamPage},

]

</script>

<DataServices></DataServices>

<main>


  <Router>

    <nav>
      <ul>
        {#each tabs as tab}
          <li><Link to={tab.route}>{tab.name}</Link></li>
        {/each}
      </ul>
    </nav>

    {#each tabs as tab }
      <Route path={tab.route}>
        <svelte:component this={tab.component} /> 
      </Route>      
    {/each}
  </Router>

</main>

<style>
  nav {
      background-color: #f8f9fa;
      padding: 10px;
    }
  
    ul {
      display: flex;
      justify-content: space-around;
      list-style-type: none;
  
    }
  
    li {
      cursor: pointer;
      margin-left: 100px;
      margin-right: 100px;
  
    }

</style>