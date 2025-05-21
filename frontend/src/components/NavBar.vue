<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light" style="position: sticky;">
        <div class="container-fluid">
            <router-link class="navbar-brand" to="/">Library</router-link>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul v-if="loggedin" class="navbar-nav ms-auto">
                    <li v-if="librarian" class="nav-item">
                        <router-link class="nav-link" to="/create-section">Create Section</router-link>
                    </li>
                    <li v-if="user" class="nav-item">
                        <router-link class="nav-link" to="#">{{ user.name }}</router-link>
                    </li>
                    <li class="nav-item">
                        <button class="nav-link" @click="logout">Logout</button>
                    </li>
                </ul>
                <ul v-else class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <router-link class="nav-link" to="/register">Register</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" to="/login">Login</router-link>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</template>

<script>
import userMixin from '@/mixins/userMixin';
export default {
    name: 'NavBar',
    mixins: [userMixin]
}
</script>