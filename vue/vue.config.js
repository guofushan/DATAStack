module.exports = {
  devServer: {
    proxy: {
      '/api': {
        // target: 'http://localhost:5001',
        target: 'http://10.88.28.3:5006',
        ws: true,
        changeOrigin: true
      }
    }
  }
}


