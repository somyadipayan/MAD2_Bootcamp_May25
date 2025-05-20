<template>
    <NavBar />
    <div class="container mt-5">
        <h2 class="text-center mb-3">All Sections</h2>
        <router-link to="/sections/create" class="btn btn-outline-primary mb-4">Create Section</router-link>
        <div v-if="sections.length === 0" class="alert alert-info">No sections found</div>
        <div v-else class="row">
        <div v-for="section in sections" :key="section.id" class="card col-md-3 mb-3">
            <div class="card-body">
                <h5 class="card-title">{{ section.name }}</h5>
                <p class="card-text">{{ section.description }}</p>
                <p v-if="section.books" class="card-text">Books: {{ section.books.length || 'No books' }}</p>
                <div class="btn btn-group">
                <router-link :to="'sections/edit/' + section.id" class="btn btn-primary">Edit Section</router-link>
                <button @click="deleteSection(section.id)" class="btn btn-danger">Delete Section</button>
                </div>
            </div>
        </div>
        </div>
    </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue'
export default {
    name: 'AllSections',
    data() {
        return {
            sections: []
        }
    },
    components: {
        NavBar
    },
    async created() {
        await this.getSections()
    },
    methods: {
        async getSections() {
            const response = await fetch('http://127.0.0.1:5000/sections', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('access_token')
                }
            })
            const data = await response.json()
            this.sections = data.sections
            console.log(this.sections)
        },
        async deleteSection(id) {
            const response = await fetch('http://127.0.0.1:5000/sections/' + id, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('access_token')
                }
            })
            const data = await response.json()
            if (response.ok) {
                alert(data.message)
                
            } else {
                alert(data.error)
            }
        }
    } 
}
</script>
