<template>
  <div id="app">
    <el-container>
      <el-header id="header">
        <el-breadcrumb separator-class="el-icon-arrow-right">
          <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
          <el-breadcrumb-item>Linux主机安全检测工具</el-breadcrumb-item>
        </el-breadcrumb>
      </el-header>
      <el-main>
        <el-form ref="form" :model="form" label-width="80px">
          <el-form-item label="IP">
            <el-input v-model="form.ip" size="medium" placeholder="请输入IP"></el-input>
          </el-form-item>
          <el-form-item label="端口">
            <el-input v-model="form.port" size="medium" placeholder="请输入端口"></el-input>
          </el-form-item>
          <el-form-item label="用户名">
            <el-input v-model="form.username" size="medium" placeholder="请输入用户名"></el-input>
          </el-form-item>
          <el-form-item label="密码">
            <el-input v-model="form.password" size="medium" placeholder="请输入密码"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="onSubmit">测试链接</el-button>
            <el-button type="primary">下发任务</el-button>
          </el-form-item>
        </el-form>
      </el-main>
    </el-container>
  </div>
</template>

<script>
export default {
  name: 'App',
  data () {
    return {
      form: {
        ip: '',
        port: 22,
        username: '',
        password: ''
      }
    }
  },
  methods: {
    onSubmit () {
      this.$http.post('/test', this.form, {emulateJSON: true})
        .then(
          (response) => {
            this.$message({
              message: '测试成功',
              type: 'success'
            })
          },
          (error) => {
            this.$message.error('连接测试失败')
          }
        )
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

#header {
  margin: 24px;
}
</style>
