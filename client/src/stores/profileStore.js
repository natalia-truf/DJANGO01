import { defineStore } from "pinia";
import { ref, onBeforeMount } from 'vue';
import axios from 'axios';
import Cookies from "js-cookie";

const useProfileStore = defineStore('profileStore', () => {

    const isAuthenticated = ref(false);
    const userName = ref(null);
    const userRole = ref(null);
    
    async function fetchMe() {
        try {
            const r = await axios.get("/api/profile/me/");
            axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
            isAuthenticated.value = r.data.is_authenticated;
            userName.value = r.data.is_authenticated ? r.data.username : null;
            userRole.value = r.data.is_authenticated ? r.data.role : null;
        } catch (e) {
            console.error(e);
        }
    }

    async function login(username, password) {
        await axios.post('/api/profile/login/', {
            username: username,
            password: password,
        })
        await fetchMe();
    }

    async function logout() {
        await axios.post("/api/profile/logout/")
        await fetchMe();
    }

    onBeforeMount(() => {
        fetchMe();
    })

    return {
        isAuthenticated,
        userName,
        userRole,
        fetchMe,
        login,
        logout,
    }
})

export default useProfileStore;