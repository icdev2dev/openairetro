
import { writable } from 'svelte/store';

// Create a writable store to hold active assistants
export const activeAssistants = writable([]);
export const currentModels = writable([])


export const url = "http://127.0.0.1:5000"

// Function to fetch active assistants from the backend
async function fetchActiveAssistants() {
    const response = await fetch(url+ `/get_active_assistants`);
    if (response.ok) {
        const data = await response.json();
        activeAssistants.set(data)
    } else {
        activeAssistants.set(['Error fetching data']);
    }
}

// Function to fetch active assistants from the backend
async function fetchCurrentModels() {
    const response = await fetch(url+ `/get_current_models`);
    if (response.ok) {
        const data = await response.json();
        currentModels.set(data)
    } else {
        currentModels.set(['Error fetching data']);
    }
}


export async function fetchAllData() {
    await fetchActiveAssistants()
    await fetchCurrentModels()

}
