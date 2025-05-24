<template>
        <div class="min-h-screen bg-gray-100 p-4 sm:p-6 lg:p-8">
            <div class="max-w-7xl mx-auto">
                <header class="bg-white rounded-lg shadow-md p-6 mb-8">
                    <h1 class="text-3xl font-bold text-gray-800 text-center sm:text-left">Librarian Dashboard</h1>
                    <p class="text-gray-600 mt-2 text-center sm:text-left">Overview of library statistics and issue trends.</p>
                </header>

                <section class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                    <div class="bg-white rounded-lg shadow-md p-6 flex flex-col items-center justify-center text-center">
                        <div class="text-5xl font-bold text-blue-600 mb-2">{{ dashboardData.total_users }}</div>
                        <h2 class="text-xl font-semibold text-gray-700">Total Users</h2>
                        <p class="text-gray-500 text-sm">Registered members</p>
                    </div>

                    <div class="bg-white rounded-lg shadow-md p-6 flex flex-col items-center justify-center text-center">
                        <div class="text-5xl font-bold text-green-600 mb-2">{{ dashboardData.total_books }}</div>
                        <h2 class="text-xl font-semibold text-gray-700">Total Books</h2>
                        <p class="text-gray-500 text-sm">Available in library</p>
                    </div>

                    <div class="bg-white rounded-lg shadow-md p-6 flex flex-col items-center justify-center text-center">
                        <div class="text-5xl font-bold text-purple-600 mb-2">{{ dashboardData.total_issues }}</div>
                        <h2 class="text-xl font-semibold text-gray-700">Total Issues</h2>
                        <p class="text-gray-500 text-sm">All time issues</p>
                    </div>
                </section>

                <section class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <div class="bg-white rounded-lg shadow-md p-6 flex flex-col items-center">
                        <h2 class="text-xl font-semibold text-gray-700 mb-4">Issue Status Distribution</h2>
                        <img
                            v-if="dashboardData.pie_image"
                            :src="dashboardData.pie_image"
                            alt="Issue Status Pie Chart"
                            class="w-full max-w-md h-auto rounded-lg"
                        />
                        <div v-else class="text-gray-500">Pie chart not available.</div>
                    </div>

                    <div class="bg-white rounded-lg shadow-md p-6 flex flex-col items-center">
                        <h2 class="text-xl font-semibold text-gray-700 mb-4">Number of Issues per Section</h2>
                        <img
                            src="http://localhost:5000/librarian/bar_chart"
                            alt="Issues per Section Bar Chart"
                            class="w-full max-w-md h-auto rounded-lg"
                        />
                    </div>
                </section>
            </div>
        </div>

</template>

<script>
export default {
    data() {
        return {
            dashboardData: {
                total_users: 0,
                total_books: 0,
                total_issues: 0,
                pie_image: null,
                bar_image: null
            }
        };
    },
    created(){
        this.fetchDashboardData();
    },
    methods: {
        async fetchDashboardData() {
            try {
                const response = await fetch('http://localhost:5000/librarian/dashboard',
                    {
                        method: 'GET',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': 'Bearer ' + localStorage.getItem('access_token')
                        }
                    }
                );
                const data = await response.json();
                this.dashboardData = data;
                console.log(this.dashboardData.pie_image);
            } catch (error) {
                console.error('Error fetching dashboard data:', error);
            }
        }
    }
}
</script>
