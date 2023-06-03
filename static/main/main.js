const {createApp} = Vue
const app =createApp({
    data() {
        return {

        }
    }
})
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}
app.use(ElementPlus)
   .mount('#main-layout')