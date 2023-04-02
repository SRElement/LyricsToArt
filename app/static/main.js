const { createApp } = Vue

const LyricsToArtApp = {
    data() {
        return {
            lyric: ''
        }
    },
    delimiters: ['{', '}']
}

createApp(LyricsToArtApp).mount('#app')
