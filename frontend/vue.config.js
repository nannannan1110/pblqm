const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  lintOnSave: false,  // 禁用ESLint检查
  devServer: {
    port: 8080,
    client: {
      overlay: {
        errors: true,
        warnings: false
      }
    },
    setupMiddlewares: (middlewares, devServer) => {
      // 忽略 ResizeObserver 错误
      devServer.options.devMiddleware = {
        ...devServer.options.devMiddleware,
        stats: {
          warnings: false
        }
      }

      // 捕获并忽略 ResizeObserver 错误
      if (!devServer.options.allowedHosts) {
        devServer.options.allowedHosts = 'all';
      }

      return middlewares
    },
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        pathRewrite: {
          '^/api': '/api'
        }
      }
    }
  },
  configureWebpack: {
    ignoreWarnings: [
      /ResizeObserver loop completed with undelivered notifications/
    ]
  }
})
