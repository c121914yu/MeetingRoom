<template>
  <div id="app">
     <router-view></router-view>
  </div>
</template>

<script>
  global.Router = (that,name) => that.$router.push({name:name})
  global.showToast = (that,text,icon) =>{
    that.$toast({
      message : text,
      icon : icon,
      duration : 1500,
      closeOnClick : true,
      position : 'middle'
    })
  }
  global.showLoading = (that,text) => {
    that.$toast.loading({
      message: text,
      forbidClick: true,
      loadingType: 'spinner',
      position : 'middle'
    })
  }
</script>

<style>
  *{
    font-size: 17px;
    padding: 0;
    margin: 0;
    box-sizing: border-box;
  }
</style>
