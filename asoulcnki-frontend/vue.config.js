module.exports = {
    chainWebpack: config => {
        config.module.rule('url-loader').test(/\.(cur)(\?.*)?$/).use('url-loader').loader('url-loader').end();
    }
}