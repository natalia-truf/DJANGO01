<script setup>
import useProfileStore from '@/stores/profileStore';
import { ref, computed, watch } from 'vue';

const profileStore = useProfileStore();

const props = defineProps({
  modelValue: Boolean,
  title: { type: String, default: 'Подтверждение OTP' }
});

const emit = defineEmits(['update:modelValue', 'success']);

const otpCode = ref('');
const errorMessage = ref('');
const isLoading = ref(false);
const isSetupMode = ref(false);
const qrCode = ref('');
const manualKey = ref('');

const isOpen = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
});

async function onSubmit() {
  errorMessage.value = '';
  isLoading.value = true;
  
  try {
    const success = await profileStore.verifyOtp(otpCode.value);
    if (success) {
      isOpen.value = false;
      otpCode.value = '';
      emit('success');
    } else {
      errorMessage.value = 'Неверный код. Попробуйте ещё раз.';
    }
  } catch (error) {
    errorMessage.value = 'Ошибка проверки кода';
  } finally {
    isLoading.value = false;
  }
}

async function onSetup() {
  isLoading.value = true;
  try {
    const data = await profileStore.setupOtp();
    qrCode.value = data.qr_code;
    manualKey.value = data.manual_key;
    isSetupMode.value = true;
  } catch (error) {
    errorMessage.value = 'Ошибка генерации ключа';
  } finally {
    isLoading.value = false;
  }
}

function closeModal() {
  isOpen.value = false;
  otpCode.value = '';
  errorMessage.value = '';
  isSetupMode.value = false;
  qrCode.value = '';
  manualKey.value = '';
}

watch(isOpen, (val) => {
  if (!val) {
    isSetupMode.value = false;
    qrCode.value = '';
    manualKey.value = '';
  }
});
</script>

<template>
  <div v-if="isOpen" class="modal fade show d-block" tabindex="-1" @click.self="closeModal">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">{{ title }}</h5>
          <button type="button" class="btn-close" @click="closeModal"></button>
        </div>
        <div class="modal-body">
          <!-- Режим настройки OTP (показывает QR-код) -->
          <div v-if="isSetupMode">
            <p>Отсканируйте QR-код в приложении Google Authenticator:</p>
            <div class="text-center mb-3">
              <img :src="qrCode" alt="QR Code" class="img-fluid border rounded p-2" style="max-width: 250px;" />
            </div>
            <p class="text-muted small">Или введите ключ вручную:</p>
            <div class="alert alert-info text-center font-monospace">
              {{ manualKey }}
            </div>
            <p class="text-muted small">После настройки приложения введите 6-значный код ниже:</p>
          </div>

          <!-- Режим ввода кода -->
          <div v-else>
            <p>Введите 6-значный код из приложения-аутентификатора:</p>
          </div>

          <div v-if="errorMessage" class="alert alert-danger mt-2">
            {{ errorMessage }}
          </div>

          <div class="mt-3">
            <input 
              v-model="otpCode" 
              type="text" 
              maxlength="6" 
              class="form-control text-center fs-4" 
              placeholder="000000"
              inputmode="numeric"
              pattern="[0-9]*"
              @keyup.enter="onSubmit"
              :disabled="isLoading"
            />
          </div>
        </div>
        <div class="modal-footer">
          <button v-if="!isSetupMode" type="button" class="btn btn-outline-secondary" @click="onSetup">
            Настроить OTP
          </button>
          <button type="button" class="btn btn-secondary" @click="closeModal">Отмена</button>
          <button v-if="!isSetupMode" type="button" class="btn btn-primary" @click="onSubmit" :disabled="isLoading || otpCode.length !== 6">
            {{ isLoading ? 'Проверка...' : 'Подтвердить' }}
          </button>
        </div>
      </div>
    </div>
  </div>
  <div v-if="isOpen" class="modal-backdrop fade show"></div>
</template>