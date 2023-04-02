const { createApp } = Vue

const Lyrics = {
    data() {
        return {
            songPlayingInfo: {},
            lyric: {},
            lyrics: "Please wait...",
            playState: {}

        }
    },
    async created() {

        let binarySearch = function (arr, currTime, start, end) {
            if (start > end) return false;

            let mid = Math.floor((start + end) / 2);

            if (arr[mid] <= currTime && arr[mid + 1] >= currTime) return arr[mid];

            if (arr[mid] > currTime)
                return binarySearch(arr, currTime, start, mid - 1);
            else
                return binarySearch(arr, currTime, mid + 1, end);
        }

        await this.getLyrics()

        while (true) {
            await this.getSongInfo()
            await this.getPlayback()

            if (this.playState["is_playing"] == true) {
                timeSampsMs = this.lyrics["time_stamps_ms"]
                progressMs = this.playState["progress_ms"]

                currLyricTimeStampMs = binarySearch(timeSampsMs, progressMs, 0, timeSampsMs.length - 1)
                if (currLyricTimeStampMs != false) {
                    this.lyric = this.lyrics[currLyricTimeStampMs]
                }

            }
        }
    },
    methods: {
        async getLyrics() {
            const response = await fetch("/getLyrics", {
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
