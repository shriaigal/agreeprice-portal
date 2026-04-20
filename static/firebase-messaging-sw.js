importScripts('https://www.gstatic.com/firebasejs/10.3.1/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/10.3.1/firebase-messaging-compat.js');

firebase.initializeApp({
  apiKey: "AIzaSyB38AwREeX86Zbib4lYKq2c-kvDhChngL0",
  authDomain: "agreepriceportal-34ac4dea.firebaseapp.com",
  projectId: "agreepriceportal-34ac4dea",
  messagingSenderId: "1077387317560",
  appId: "1:1077387317560:web:a1f4c3044c965d9e07f1cd"
});

const messaging = firebase.messaging();

messaging.onBackgroundMessage(function(payload) {
  console.log('[firebase-messaging-sw.js] Received background message ', payload);
  const notificationTitle = payload.notification.title;
  const notificationOptions = {
    body: payload.notification.body,
    icon: '/static/icon.png'
  };

  self.registration.showNotification(notificationTitle, notificationOptions);
});
