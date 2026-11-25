<script setup>
import useProfileStore from '@/stores/profileStore';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const profileStore = useProfileStore();
const router = useRouter();

const isRegisterMode = ref(false);

const username = ref("");
const password = ref("");
const role = ref("buyer");
const errorMessage = ref("");

async function onSubmit() {
    errorMessage.value = "";
    
    if (isRegisterMode.value) {
        const result = await profileStore.register(username.value, password.value, role.value);
        if (result.success) {
            router.push('/products');
        } else {
            errorMessage.value = result.error || "Ошибка регистрации";
        }
    } else {
        await profileStore.login(username.value, password.value);
        if (profileStore.isAuthenticated) {
            router.push('/products');
        } else {
            errorMessage.value = "Неверный логин или пароль";
        }
    }
}

function toggleMode() {
    isRegisterMode.value = !isRegisterMode.value;
    errorMessage.value = "";
    username.value = "";
    password.value = "";
}
</script>

<template>
    <div class="d-flex justify-content-center align-items-center" style="min-height: 80vh;">
        <div class="card p-4" style="width: 400px;">
            <h3 class="text-center mb-4">{{ isRegisterMode ? 'Регистрация' : 'Вход в систему' }}</h3>
            
            <div v-if="errorMessage" class="alert alert-danger">
                {{ errorMessage }}
            </div>

            <form @submit.prevent="onSubmit">
                <div class="mb-3">
                    <label class="form-label">Логин</label>
                    <input v-model="username" required type="text" class="form-control" placeholder="Введите логин">
                </div>
                
                <div class="mb-3">
                    <label class="form-label">Пароль</label>
                    <input v-model="password" required type="password" class="form-control" placeholder="Введите пароль">
                </div>

                <div v-if="isRegisterMode" class="mb-3">
                    <label class="form-label">Роль</label>
                    <select v-model="role" class="form-select">
                        <option value="buyer">Покупатель</option>
                        <option value="seller">Продавец</option>
                    </select>
                </div>

                <button class="btn btn-primary w-100 mb-3">
                    {{ isRegisterMode ? 'Зарегистрироваться' : 'Войти' }}
                </button>
            </form>

            <div class="text-center">
                <button class="btn btn-link text-decoration-none" @click="toggleMode">
                    {{ isRegisterMode ? 'Уже есть аккаунт? Войти' : 'Нет аккаунта? Зарегистрироваться' }}
                </button>
            </div>
        </div>
    </div>
</template>