import { defineStore } from "pinia";
import { ref, onBeforeMount } from 'vue';
import axios from 'axios';
import Cookies from "js-cookie";

const useProfileStore = defineStore('profileStore', () => {
    const isAuthenticated = ref(false);
    const userName = ref(null);
    const userRole = ref(null);
    const isSuperuser = ref(false);
    const otpEnabled = ref(false);
    const otpVerified = ref(false);
    const isLoaded = ref(false);
    
    async function fetchMe() {
        const r = await axios.get("/api/profile/me/");
        axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
        isAuthenticated.value = r.data.is_authenticated;
        userName.value = r.data.is_authenticated ? r.data.username : null;
        userRole.value = r.data.is_authenticated ? r.data.role : null;
        isSuperuser.value = r.data.is_authenticated ? r.data.is_superuser : false;
        otpEnabled.value = r.data.is_authenticated ? (r.data.otp_enabled || false) : false;
        isLoaded.value = true;
    }

    async function login(username, password) {
        await axios.post('/api/profile/login/', { username, password })
        await fetchMe();
    }

    async function logout() {
        await axios.post("/api/profile/logout/")
        await fetchMe();
    }

    async function checkOtpStatus() {
        const r = await axios.get("/api/profile/otp-status/");
        otpVerified.value = r.data.otp_good;
        return otpVerified.value;
    }

    async function verifyOtp(code) {
        const r = await axios.post("/api/profile/otp-login/", { key: code });
        if (r.data.success) {
            otpVerified.value = true;
        }
        return r.data.success;
    }

    async function setupOtp() {
        const r = await axios.get("/api/profile/otp-setup/");
        return r.data;
    }

    async function disableOtp() {
        await axios.post("/api/profile/otp-disable/");
        otpEnabled.value = false;
        otpVerified.value = false;
    }

    onBeforeMount(() => {
        fetchMe();
        if (isAuthenticated.value) {
            checkOtpStatus();
        }
    })

    return {
        isAuthenticated, userName, userRole, isSuperuser, otpEnabled, otpVerified, isLoaded,
        fetchMe, login, logout,
        checkOtpStatus, verifyOtp, setupOtp, disableOtp,
    }
})

export default useProfileStore;