<script setup>
import useProfileStore from '@/stores/profileStore';
import { storeToRefs } from 'pinia';

const profileStore = useProfileStore();
const { isAuthenticated, userName } = storeToRefs(profileStore)

async function onLogoutButtonClick() {
    profileStore.logout();
}
</script>

<template>
    <nav class="navbar navbar-expand-sm bg-body-tertiary">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">Navbar</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse w-100 justify-content-between" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item"><router-link class="nav-link" to="/products">Товары</router-link></li>
                    <li class="nav-item"><router-link class="nav-link" to="/categories">Категории</router-link></li>
                    <li class="nav-item"><router-link class="nav-link" to="/suppliers">Поставщики</router-link></li>
                    <li class="nav-item"><router-link class="nav-link" to="/points">Точки продажи</router-link></li>
                    <li class="nav-item"><router-link class="nav-link" to="/orders">Заказы</router-link></li>
                    <li class="nav-item"><router-link class="nav-link" to="/login">Вход</router-link></li>
                    <li class="nav-item"><a class="nav-link" href="/admin">Админка</a></li>
                </ul>
                <div role="search">
                    Авторизован: {{ userName }}
                    <button v-if="isAuthenticated" class="btn btn-outline-success" @click="onLogoutButtonClick">
                        Выйти
                    </button>
                </div>
            </div>
        </div>
    </nav>
</template>