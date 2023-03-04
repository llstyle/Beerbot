var app = new Vue({
    el: '#app',
    data: {
      uname: 'Unauthorizited',
      info: [],
      username: '',
      password: '',
      authenticated: false,
    },
    methods: {
      async get_me(token) {
        let username = ''
        await axios.get('/users/me/', {
          headers: {
            "Authorization": `Bearer ${token}`,
          },
        })
        .then(response => {
          console.log(response.data.username)
          username = response.data.username
        })
        .catch(error => {
          alert("please login")
        })
        return username
      },
      auth() {
        const bodyFormData = new FormData();
        bodyFormData.append("username", this.username)
        bodyFormData.append("password", this.password)
        axios.post('/token', bodyFormData, {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
        })
        .then(response => {
          localStorage.setItem('token', response.data.access_token)
          document.location.reload();
        })
        this.password = ''
        this.username = ''
      },
      add() {
        let parentId = this.$refs.parentAdd.value ? this.$refs.parentAdd.value : null
        let title = this.$refs.titleAdd.value
        let text = this.$refs.add['data-froala.editor'].html.get()
        axios.post('/faq_create/', {
          title: title,
          text: text,
          parent_id: parentId
        }, {
          headers: {
            "Authorization": `Bearer ${localStorage.getItem('token')}`,
          },
        })
        .then(response => {
          document.location.reload();
        })
      },
    editFaq() {
      let title = this.$refs.titleFaq.value
      let id = this.$refs.idFaq.value
      let text = this.$refs.edit['data-froala.editor'].html.get()
      axios.put(`/update/${id}`, {
        title: title,
        text: text,
      }, {
        headers: {
          "Authorization": `Bearer ${localStorage.getItem('token')}`,
        },
      })
      .then(response => {
        document.location.reload();
      })
    },
  },

    async mounted () {
      let username =  await this.get_me(localStorage.getItem('token'))
      if (username) {
        this.uname = username
        axios
          .get('/faq_get_all/')
          .then(response => (this.info = response.data))
        this.authenticated = true
      }
    }
  })

Vue.component("faq-item", {
  template: "#item-template",
  props: {
    child: Object
  },
  methods: {
    deleteFaq(id) {
      axios.delete(`/delete/${id}`, {
        headers: {
          "Authorization": `Bearer ${localStorage.getItem('token')}`,
        },
      })
      .then(response => {
        document.location.reload();
      })
    }
  }
})
