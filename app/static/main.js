const { createApp } = Vue

const Lyrics = {
    data() {
        return {
            songPlayingInfo: {},
            lyric: 'Lyrics here',
            lyrics: "Please wait...",
            playState: {},
            currArtistName: '',
            currSongTitle: '',
            songFound: false

        }
    },
    async created() {

        let binarySearch = function (arr, currTime, start, end) {
            if (start > end) return false; //Neccisarry?

            let mid = Math.floor((start + end) / 2);

            if (arr[mid] <= currTime && arr[mid + 1] >= currTime) return arr[mid];

            if (arr[mid] > currTime)
                return binarySearch(arr, currTime, start, mid - 1);
            else
                return binarySearch(arr, currTime, mid + 1, end);
        }


        while (true) {
            await this.getSongInfo()
            await this.getPlayback()

            if (this.playState["is_playing"] == true) {

                if (this.songPlayingInfo["artist_name"] != this.currArtistName || this.songPlayingInfo["song_title"] != this.currSongTitle) {

                    this.lyric = 'Searching...'
                    this.currSongTitle = this.songPlayingInfo["song_title"]
                    this.currArtistName = this.songPlayingInfo["artist_name"]

                    await this.getLyrics()
                    if (Object.keys(this.lyrics).length === 0 && this.lyrics.constructor === Object) {
                        this.songFound = false
                    } else {
                        this.songFound = true
                    }
                }

                if (this.songFound == true) {

                    timeSampsMs = this.lyrics["time_stamps_ms"]
                    progressMs = this.playState["progress_ms"]

                    currLyricTimeStampMs = binarySearch(timeSampsMs, progressMs, 0, timeSampsMs.length - 1)
                    if (currLyricTimeStampMs != false) {
                        this.lyric = this.lyrics[currLyricTimeStampMs]
                    }
                } else {
                    this.lyric = 'Lyrics cant be found'
                }

            }
        }
    },
    methods: {
        async getLyrics() {
            url = "/getLyrics/" + this.songPlayingInfo["artist_name"] + "/" + this.songPlayingInfo["song_title"]
            const response = await fetch(url, {
                method: 'get',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })

            this.lyrics = await response.json()
        },
        async getPlayback() {
            const response = await fetch("/getPlayback", {
                method: 'get',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })

            this.playState = await response.json()
        },
        async getSongInfo() {
            const response = await fetch("/getSongInfo", {
                method: 'get',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })

            this.songPlayingInfo = await response.json()
        }
    },
    delimiters: ['{', '}']
}

createApp(Lyrics).mount('#Lyrics')
