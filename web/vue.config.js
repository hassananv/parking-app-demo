const webBaseHref = process.env.WEB_BASE_HREF || '/parking-app';
module.exports = {
  publicPath: webBaseHref,
  devServer: {
    proxy: {
      "/api": {
        target: "http://localhost:8080",
        pathRewrite: { '^/parking-app': '' },
        secure: false,
        changeOrigin: true,
        headers: {
		      "X-Forwarded-Host": "localhost:8081",
          Connection: 'keep-alive'
        },
      }
    }
  },
  chainWebpack: config => {
    config.module.rules.delete("eslint");
    config.module
	 .rule('vue')
      .use('vue-loader')
        .tap(options => {
          options.prettify = false
          return options
        });
      config.module.rule("ts")
      .test(/\.ts$/)
      .use("ts-loader")
      .loader("ts-loader")
      .options({
        appendTsSuffixTo: [/\.vue$/],
        transpileOnly: true
      });
  },
  parallel: false
};
