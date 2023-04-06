const { createApp } = Vue

const Lyrics = {
    data() {
        return {
            songPlayingInfo: {},
            lyricImgs: {},
            currImg: '',
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

                if (this.songPlayingInfo["artist_name"] == null || this.songPlayingInfo["song_title"] == null) {
                    this.songFound = false
                }
                else if (this.songPlayingInfo["artist_name"] != this.currArtistName || this.songPlayingInfo["song_title"] != this.currSongTitle) {

                    this.lyric = 'Searching...'
                    this.currSongTitle = this.songPlayingInfo["song_title"]
                    this.currArtistName = this.songPlayingInfo["artist_name"]

                    await this.getLyrics()
                    if (Object.keys(this.lyrics).length === 0 && this.lyrics.constructor === Object) {
                        this.songFound = false
                    } else {
                        this.songFound = true
                        await this.getSongImages()
                    }
                }

                if (this.songFound == true) {

                    timeSampsMs = this.lyrics["time_stamps_ms"]
                    progressMs = this.playState["progress_ms"]

                    currLyricTimeStampMs = binarySearch(timeSampsMs, progressMs, 0, timeSampsMs.length - 1)
                    if (currLyricTimeStampMs != false) {
                        this.lyric = this.lyrics[currLyricTimeStampMs]

                        newImg = this.lyricImgs[this.lyric['hash_id']]
                        if (newImg != this.currImg) {
                            this.currImg = this.lyricImgs[this.lyric['hash_id']]
                        }
                    }
                } else {
                    this.lyric = 'Lyrics cant be found'
                    this.currImg = ''
                    this.lyricImgs = {}
                }

            }
        }
    },
    methods: {
        async getLyrics() {
            url = "/getLyrics/" + this.songPlayingInfo["artist_name"] + "/" + this.songPlayingInfo["song_title"] + "/" + this.songPlayingInfo["song_id"]
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
        },

        async getSongImages() {
            url = "/getSongImages/" + this.songPlayingInfo["song_id"]
            const response = await fetch(url, {
                method: 'get',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })

            this.lyricImgs = await response.json()
        }

    },
    delimiters: ['{', '}']
}

createApp(Lyrics).mount('#Lyrics')
