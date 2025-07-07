<template lang="pug">
  .wrapper
    .datetime-container
      .date-display {{ formattedDate }}
      .time-display {{ formattedTime }}
    .attendance-controls
      button( @click="recordAttendance" :disabled="isLoadingClockIn" ) {{ isLoadingClockIn ? '処理中...' : '出勤' }}
      button( @click="recordLeaving" :disabled="isLoadingClockOut" ) {{ isLoadingClockOut ? '処理中...' : '退勤' }}
    .api-message( v-if="apiMessage" :class="{ success: isSuccessMessage, error: !isSuccessMessage }" ) {{ apiMessage }}
    .attendance-log
      p( v-if="attendanceTime" ) 出勤時刻: {{ formattedAttendanceTime }}
      p( v-if="leavingTime" ) 退勤時刻: {{ formattedLeavingTime }}
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import axios from 'axios'
import { ATENDANCE_BASE_URL } from '@/utils/endpoints'

const now = ref(new Date())
let timerId: number | undefined = undefined
const attendanceTime = ref<Date | null>(null)
const leavingTime = ref<Date | null>(null)
const isLoadingClockIn = ref(false)
const isLoadingClockOut = ref(false)
const apiMessage = ref('')
const isSuccessMessage = ref(false)

const formattedDate = computed(() => {
  return now.value.toLocaleString('ja-JP', {
    timeZone: 'Asia/Tokyo',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    weekday: 'long',
  })
})

const formattedTime = computed(() => {
  return now.value.toLocaleString('ja-JP', {
    timeZone: 'Asia/Tokyo',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false,
  })
})

const formatRecordTime = (date: Date | null): string => {
  if (!date) return ''
  return date.toLocaleString('ja-JP', {
    timeZone: 'Asia/Tokyo',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false,
  })
}
const formattedAttendanceTime = computed(() => formatRecordTime(attendanceTime.value))
const formattedLeavingTime = computed(() => formatRecordTime(leavingTime.value))


const updateTime = () => {
  now.value = new Date()
}

const recordAttendance = async () => {
  isLoadingClockIn.value = true
  apiMessage.value = ''
  isSuccessMessage.value = false
  try {
    const response = await axios.post(`${ATENDANCE_BASE_URL}/clock-in`)
    if (response.data && response.data.stamp_time) {
      attendanceTime.value = new Date(response.data.stamp_time)
    } else {
      attendanceTime.value = new Date()
    }
    leavingTime.value = null
    apiMessage.value = '出勤時刻を記録しました。'
    isSuccessMessage.value = true
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      apiMessage.value = `エラー[${error.response.status}]: ${error.response.data?.detail || '出勤記録に失敗しました。'}`
    } else {
      apiMessage.value = 'エラー: 出勤記録に失敗しました。'
    }
    isSuccessMessage.value = false
  } finally {
    isLoadingClockIn.value = false
  }
}

const recordLeaving = async () => {
  isLoadingClockOut.value = true
  apiMessage.value = ''
  isSuccessMessage.value = false
  try {
    const response = await axios.post(`${ATENDANCE_BASE_URL}/clock-out`)
    if (response.data && response.data.stamp_time) {
      leavingTime.value = new Date(response.data.stamp_time)
    } else {
      leavingTime.value = new Date()
    }
    apiMessage.value = '退勤時刻を記録しました。'
    isSuccessMessage.value = true
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      apiMessage.value = `エラー[${error.response.status}]: ${error.response.data?.detail || '退勤記録に失敗しました。'}`
    } else {
      apiMessage.value = 'エラー: 退勤記録に失敗しました。サーバー接続を確認してください。'
    }
    isSuccessMessage.value = false
  } finally {
    isLoadingClockOut.value = false
  }
}

onMounted(() => {
  updateTime()
  timerId = window.setInterval(updateTime, 1000)
  console.log('AttendanceSystem.vue がマウントされました。')
})

onUnmounted(() => {
  if (timerId) {
    clearInterval(timerId)
  }
})
</script>

<style scoped>
main {
  line-height: 1.5;
  display: flex;
  justify-content: center;
  min-height: 100vh;
  width: 100%;
}
.wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  padding-top: 2em;
}
.datetime-container {
  display: flex;
  flex-direction: column;
  margin-bottom: 1em;
}
.date-display {
  text-align: center;
  font-size: 1.8em;
  line-height: 1.3;
  margin-bottom: 0.1em;
}
.time-display {
  text-align: center;
  font-size: 2em;
}
.attendance-controls {
  display: flex;
  gap: 1em;
  margin-bottom: 1em;
}
.attendance-controls button {
  padding: 0.5em 1em;
  font-size: 1em;
  cursor: pointer;
}
.attendance-log {
  text-align: center;
  margin-top: 1em;
  font-size: 1em;
  border: 1px solid #ccc;
  padding: 1.5em;
  border-radius: 8px;
  min-width: 300px;
  background-color: #f8f8f8;
}
.attendance-log p {
  margin: 0.5em 0;
}
</style>
