// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyB62hjok7CTknjPJk5N66yZvmJfMeBQcpc",
  authDomain: "my-project-420-353715.firebaseapp.com",
  databaseURL: "https://my-project-420-353715-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "my-project-420-353715",
  storageBucket: "my-project-420-353715.appspot.com",
  messagingSenderId: "1067997670534",
  appId: "1:1067997670534:web:e0a3ddc25633189a207507",
  measurementId: "G-C5VC6M3P6Z"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);