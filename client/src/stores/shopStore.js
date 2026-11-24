import { defineStore } from "pinia";
import { ref, onBeforeMount } from "vue";
import axios from "axios";

const useShopStore = defineStore("ShopStore", () => {
    const products = ref([]);
    const categories = ref([]);
    const suppliers = ref([]);
    const points = ref([]);
    const orders = ref([]);

    const allCategories = ref([]);
    const allSuppliers = ref([]);
    const allPoints = ref([]);
    const allProducts = ref([]);

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

    const productsFilter = ref({ name: '', category: '', supplier: '', priceFrom: '', priceTo: '' });
    const categoriesFilter = ref({ name: '' });
    const suppliersFilter = ref({ name: '', phone: '' });
    const pointsFilter = ref({ name: '', address: '' });
    const ordersFilter = ref({ 
        product: '', 
        point: '', 
        orderId: '', 
        quantity: '', 
        totalPriceFrom: '', 
        totalPriceTo: '' 
    });

    async function fetchAllCategories() {
        const r = await axios.get("/api/categories/");
        allCategories.value = r.data.results || r.data;
    }

    async function fetchAllSuppliers() {
        const r = await axios.get("/api/suppliers/", { params: { page_size: 10000 } });
        allSuppliers.value = r.data.results || r.data;
    }

    async function fetchAllPoints() {
        const r = await axios.get("/api/points/", { params: { page_size: 10000 } });
        allPoints.value = r.data.results || r.data;
    }

    async function fetchAllProducts() {
        const r = await axios.get("/api/products/", { params: { page_size: 10000 } });
        allProducts.value = r.data.results || r.data;
    }

    async function fetchProducts() {
    const r = await axios.get("/api/products/", { 
        params: { 
            page: productsPage.value, 
            name: productsFilter.value.name,
            category: productsFilter.value.category,
            supplier: productsFilter.value.supplier,
            price_from: productsFilter.value.priceFrom,
            price_to: productsFilter.value.priceTo
        } 
    });
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
        const r = await axios.get("/api/categories/", { 
            params: { name: categoriesFilter.value.name } 
        });
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
        fetchAllCategories();
    }
    async function removeCategory(id) {
        await axios.delete(`/api/categories/${id}/`);
        fetchCategories();
        fetchCategoriesStats();
        fetchAllCategories();
    }
    async function updateCategory(id, formData) {
        await axios.put(`/api/categories/${id}/`, formData);
        fetchCategories();
        fetchCategoriesStats();
        fetchAllCategories();
    }

    async function fetchSuppliers() {
        const r = await axios.get("/api/suppliers/", { 
            params: { 
                page: suppliersPage.value, 
                name: suppliersFilter.value.name,
                phone: suppliersFilter.value.phone
            } 
        });
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
        fetchAllSuppliers();
    }
    async function removeSupplier(id) {
        await axios.delete(`/api/suppliers/${id}/`);
        fetchSuppliers();
        fetchSuppliersStats();
        fetchAllSuppliers();
    }
    async function updateSupplier(id, data) {
        await axios.put(`/api/suppliers/${id}/`, data);
        fetchSuppliers();
        fetchSuppliersStats();
        fetchAllSuppliers();
    }

    async function fetchPoints() {
        const r = await axios.get("/api/points/", { 
            params: { 
                page: pointsPage.value, 
                name: pointsFilter.value.name,
                address: pointsFilter.value.address
            } 
        });
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
        fetchAllPoints();
    }
    async function removePoint(id) {
        await axios.delete(`/api/points/${id}/`);
        fetchPoints();
        fetchPointsStats();
        fetchAllPoints();
    }
    async function updatePoint(id, data) {
        await axios.put(`/api/points/${id}/`, data);
        fetchPoints();
        fetchPointsStats();
        fetchAllPoints();
    }

    async function fetchOrders() {
        const params = { page: ordersPage.value };

        if (ordersFilter.value.product) params.product = ordersFilter.value.product;
        if (ordersFilter.value.point) params.point = ordersFilter.value.point;
        if (ordersFilter.value.orderId) params.order_id = ordersFilter.value.orderId;
        if (ordersFilter.value.quantity) params.quantity = ordersFilter.value.quantity;
        if (ordersFilter.value.totalPriceFrom) params.price_from = ordersFilter.value.totalPriceFrom;
        if (ordersFilter.value.totalPriceTo) params.price_to = ordersFilter.value.totalPriceTo;

        const r = await axios.get("/api/orders/", { params });
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
        
        fetchAllCategories();
        fetchAllSuppliers();
        fetchAllPoints();
        fetchAllProducts();
    });

    return {
        products, categories, suppliers, points, orders,
        allCategories, allSuppliers, allPoints, allProducts,
        productsStats, suppliersStats, pointsStats, ordersStats, categoriesStats,
        
        productsPage, productsTotalCount, productsFilter,
        suppliersPage, suppliersTotalCount, suppliersFilter,
        pointsPage, pointsTotalCount, pointsFilter,
        ordersPage, ordersTotalCount, ordersFilter,
        categoriesFilter,
        pageItemsCount,

        fetchProducts, fetchProductsStats, 
        fetchCategories, fetchCategoriesStats,
        fetchSuppliers, fetchSuppliersStats, 
        fetchPoints, fetchPointsStats, 
        fetchOrders, fetchOrdersStats,
        
        fetchAllCategories, fetchAllSuppliers, fetchAllPoints, fetchAllProducts,

        addProduct, removeProduct, updateProduct,
        addCategory, removeCategory, updateCategory,
        addSupplier, removeSupplier, updateSupplier,
        addPoint, removePoint, updatePoint,
        addOrder, removeOrder, updateOrder,
        addGalleryImage, removeGalleryImage,
    };
});

export default useShopStore;