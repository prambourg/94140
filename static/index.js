Vue.component('my-nav-bar', {
    props: ['navbar'],
    template: `
        <nav class="navbar navbar-expand-lg navbar-light bg-light">
            <div class="container-fluid">
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                        <li class="nav-item" v-for="el in navbar" :key="el.label">
                            <a class="nav-link text-dark" :href="el.url">{{ el.label }}</a>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>`
  });
  
  Vue.component('my-hero', {
    props: ['isAdmin', 'urlsSubscriptions'],
    data: function() {
        return  {
            members: [],
            selectedYear: 2025,
            syncing: false,
            syncMessage: '',
        }
    },
    methods: {
        getMembers() {
          const path = window.location.origin + '/members?year=' + this.selectedYear;
          axios.get(path)
            .then((res) => {
              this.members = res.data.members;console.log(res.data)
            })
            .catch((error) => {
              console.error(error);
            });
        },
        updateYear(event) {
            this.selectedYear = event.target.value;
            this.getMembers();
        },
        syncMembers() {
            this.syncing = true;
            this.syncMessage = '';
            const path = window.location.origin + '/sync_members';
            axios.post(path)
              .then((res) => {
                this.syncing = false;
                this.syncMessage = res.data.message;
                // Refresh the members list after sync
                this.getMembers();
                // Clear message after 5 seconds
                setTimeout(() => {
                  this.syncMessage = '';
                }, 5000);
              })
              .catch((error) => {
                this.syncing = false;
                this.syncMessage = error.response?.data?.message || 'Erreur lors de la synchronisation';
                console.error(error);
                // Clear error message after 5 seconds
                setTimeout(() => {
                  this.syncMessage = '';
                }, 5000);
              });
        },
    },
    created() {
        this.getMembers();
    },
    template: `
        <div class="jumbotron container my-5 p-4 bg-light border rounded shadow">
            <div class="d-flex justify-content-between align-items-center">
                <h1 class="display-4 text-success">Liste des membres du Café des Sciences</h1>
                <button v-if="isAdmin" @click="syncMembers" :disabled="syncing" class="btn btn-primary">
                    <span v-if="syncing" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                    {{ syncing ? 'Synchronisation...' : 'Sync' }}
                </button>
            </div>
            <div v-if="syncMessage" :class="['alert', syncMessage.includes('Erreur') ? 'alert-danger' : 'alert-success', 'mt-3']" role="alert">
                {{ syncMessage }}
            </div>
            <p class="lead text-secondary">Sélectionnez une année pour voir les membres à jour pour cette période.</p>
            <hr class="my-4" />
            <div class="mb-4">
                <p class="text-secondary">Pour toute question, me contacter à <strong>contact.laminutescientifique@gmail.com</strong>.</p>
                <div class="d-flex align-items-center gap-3">
                    <div>
                        <label for="yearSelect" class="form-label text-secondary mb-0">Année :</label>
                        <select id="yearSelect" class="form-select w-auto d-inline ms-2" v-model="selectedYear" @change="updateYear">
                            <option v-for="year in [2026, 2025, 2024, 2023, 2022, 2021, 2020]" :key="year" :value="year">{{ year }}</option>
                        </select>
                    </div>
                    <a v-if="urlsSubscriptions && urlsSubscriptions[selectedYear]" :href="urlsSubscriptions[selectedYear]" target="_blank" class="btn btn-success btn-sm">
                        Cotiser pour la campagne {{ selectedYear }}
                    </a>
                </div>
            </div>
            <div class="d-flex justify-content-center">
                <div class="table-responsive">
                    <table class="table table-hover table-striped table-bordered text-center shadow-lg">
                        <thead class="table-success">
                            <tr>
                                <th scope="col">Nom</th>
                                <th scope="col">URLs</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(member, index) in members" :key="index">
                                <td>{{ member[0] }}</td>
                                <td v-html="member[1]"></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    `
  });
  
  Vue.component('my-footer', {
    props: ['owner', 'site'],
    computed: {
        name() {
            site_owner = 'You'
            for(const property in this.owner) {
                if (property == 'name') {
                    site_owner = `${this.owner[property]}`;
                    break
                }
            }
            return site_owner;
        },
        website() {
            website = ''
            for(const property in this.owner) {
                if (property == 'website') {
                    website = `${this.owner[property]}`;
                    break
                }
            }
            return website;
        }
    },
    template: `
        <footer class="footer mt-auto py-3 bg-success text-light shadow">
            <div class="container text-center">
                <span class="fw-bold">🇫🇷 {{ name }}</span>
                <a :href="website" class="text-light ms-2" target="_blank"><small>{{ website }}</small></a>
            </div>
        </footer>
    `
  });
  
  
  const app = new Vue({
      el: '#app',
  })