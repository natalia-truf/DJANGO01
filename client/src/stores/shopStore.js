import { defineStore } from "pinia";
import { ref, onBeforeMount } from "vue";
import axios from "axios";

const useShopStore = defineStore("ShopStore", () => {
    const products = ref([]);
    const categories = ref([]);
    const suppliers = ref([]);
    const points = ref([]);
    const orders = ref([]);

    const productsStats = ref({});
    const suppliersStats = ref({});
    const categoriesStats = ref({});
    const pointsStats = ref({});
    const ordersStats = ref({});

    const productsPage = ref(1);
    const productsTotalCount = ref(0);

    const suppliersPage = ref(1);
    const suppliersTotalCount = ref(0);

    const pointsPage = ref(1);
    const pointsTotalCount = ref(0);

    const ordersPage = ref(1);
    const ordersTotalCount = ref(0);

    const pageItemsCount = ref(10);

    async function fetchProducts() {
        const r = await axios.get("/api/products/", { params: { page: productsPage.value } });
        products.value = r.data.results || r.data;
        productsTotalCount.value = r.data.count || 0;
    }
    async function fetchProductsStats() {
        const r = await axios.get("/api/products/stats/");
        productsStats.value = r.data;
    }
    async function addProduct(formData) {
        await axios.post("/api/products/", formData);
        fetchProducts();
        fetchProductsStats();
    }
    async function removeProduct(id) {
        await axios.delete(`/api/products/${id}/`);
        fetchProducts();
        fetchProductsStats();
    }
    async function updateProduct(id, formData) {
        await axios.put(`/api/products/${id}/`, formData);
        fetchProducts();
        fetchProductsStats();
    }

    async function fetchCategories() {
        const r = await axios.get("/api/categories/");
        categories.value = r.data.results || r.data;
    }
    async function fetchCategoriesStats() {
        const r = await axios.get("/api/categories/stats/");
        categoriesStats.value = r.data;
    }
    async function addCategory(formData) {
        await axios.post("/api/categories/", formData);
        fetchCategories();
        fetchCategoriesStats();
    }
    async function removeCategory(id) {
        await axios.delete(`/api/categories/${id}/`);
        fetchCategories();
        fetchCategoriesStats();
    }
    async function updateCategory(id, formData) {
        await axios.put(`/api/categories/${id}/`, formData);
        fetchCategories();
        fetchCategoriesStats();
    }

    async function fetchSuppliers() {
        const r = await axios.get("/api/suppliers/", { params: { page: suppliersPage.value } });
        suppliers.value = r.data.results || r.data;
        suppliersTotalCount.value = r.data.count || 0;
    }
    async function fetchSuppliersStats() {
        const r = await axios.get("/api/suppliers/stats/");
        suppliersStats.value = r.data;
    }
    async function addSupplier(data) {
        await axios.post("/api/suppliers/", data);
        fetchSuppliers();
        fetchSuppliersStats();
    }
    async function removeSupplier(id) {
        await axios.delete(`/api/suppliers/${id}/`);
        fetchSuppliers();
        fetchSuppliersStats();
    }
    async function updateSupplier(id, data) {
        await axios.put(`/api/suppliers/${id}/`, data);
        fetchSuppliers();
        fetchSuppliersStats();
    }

    async function fetchPoints() {
        const r = await axios.get("/api/points/", { params: { page: pointsPage.value } });
        points.value = r.data.results || r.data;
        pointsTotalCount.value = r.data.count || 0;
    }
    async function fetchPointsStats() {
        const r = await axios.get("/api/points/stats/");
        pointsStats.value = r.data;
    }
    async function addPoint(data) {
        await axios.post("/api/points/", data);
        fetchPoints();
        fetchPointsStats();
    }
    async function removePoint(id) {
        await axios.delete(`/api/points/${id}/`);
        fetchPoints();
        fetchPointsStats();
    }
    async function updatePoint(id, data) {
        await axios.put(`/api/points/${id}/`, data);
        fetchPoints();
        fetchPointsStats();
    }

    async function fetchOrders() {
        const r = await axios.get("/api/orders/", { params: { page: ordersPage.value } });
        orders.value = r.data.results || r.data;
        ordersTotalCount.value = r.data.count || 0;
    }
    async function fetchOrdersStats() {
        const r = await axios.get("/api/orders/stats/");
        ordersStats.value = r.data;
    }
    async function addOrder(data) {
        await axios.post("/api/orders/", data);
        fetchOrders();
        fetchOrdersStats();
    }
    async function removeOrder(id) {
        await axios.delete(`/api/orders/${id}/`);
        fetchOrders();
        fetchOrdersStats();
    }
    async function updateOrder(id, data) {
        await axios.put(`/api/orders/${id}/`, data);
        fetchOrders();
        fetchOrdersStats();
    }

    async function addGalleryImage(formData, product) {
        await axios.post("/api/productimages/", formData);
        await fetchProducts();
    }
    async function removeGalleryImage(image) {
        await axios.delete(`/api/productimages/${image.id}/`);
        await fetchProducts();
    }

    onBeforeMount(() => {
        fetchProducts();
        fetchProductsStats();
        fetchCategories();
        fetchCategoriesStats();
        fetchSuppliers();
        fetchSuppliersStats();
        fetchPoints();
        fetchPointsStats();
        fetchOrders();
        fetchOrdersStats();
    });

    return {
        products, categories, suppliers, points, orders,
        productsStats, suppliersStats, pointsStats, ordersStats, categoriesStats,
        
        productsPage, productsTotalCount,
        suppliersPage, suppliersTotalCount,
        pointsPage, pointsTotalCount,
        ordersPage, ordersTotalCount,
        pageItemsCount,

        fetchProducts, fetchProductsStats, 
        fetchCategories, fetchCategoriesStats,
        fetchSuppliers, fetchSuppliersStats, 
        fetchPoints, fetchPointsStats, 
        fetchOrders, fetchOrdersStats,
        
        addProduct, removeProduct, updateProduct,
        addCategory, removeCategory, updateCategory,
        addSupplier, removeSupplier, updateSupplier,
        addPoint, removePoint, updatePoint,
        addOrder, removeOrder, updateOrder,
        addGalleryImage, removeGalleryImage,
    };
});

export default useShopStore;