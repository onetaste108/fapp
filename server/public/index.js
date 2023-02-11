
// Utils

const uploadFile = (callback) => {
    const input = document.createElement('input');
    input.setAttribute('type', 'file');
    input.addEventListener('input', (ev) => {
        let file = input.files[0];
        callback(file);       
    }, { once: true })
    input.click();
};

// Page

const textForm = document.getElementById("textForm");
const onText = (cb) => {
    textForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const textInput = textForm.elements["textInput"];
        let textValue = textInput.value;
        // textInput.value = "";
        cb(textValue);
    });
};

const uploadButton = document.getElementById("uploadButton");
const onFile = (cb) => {
    uploadButton.addEventListener('click', (event) => {
        uploadFile(cb);
    });
};
const likeButton = document.getElementById("likeButton");
const onLike = (cb) => {
    likeButton.addEventListener('click', cb);
};


// Canvas





// Firebase


import * as firebaseApp from 'https://www.gstatic.com/firebasejs/9.17.1/firebase-app.js';
import * as firebaseStorage from "https://www.gstatic.com/firebasejs/9.17.1/firebase-storage.js";
// import * as firebaseDatabase from "https://www.gstatic.com/firebasejs/9.8.3/firebase-database.js";
import * as firebaseFirestore from "https://www.gstatic.com/firebasejs/9.17.1/firebase-firestore.js";
// import { text } from 'express';

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


function gname(path) {
    const BUCKET_NAME = 'my-project-420-353715.appspot.com'
    var new_path = 'https://'+BUCKET_NAME+'.storage.googleapis.com/'+path;
    return new_path;
}


///////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////


const new_image = (index) => {
    console.log("Set image: ", index)
    // var docRef = db.collection("images").doc(String(index));
    var docRef = firebaseFirestore.doc(db, "images", String(index));
    firebaseFirestore.getDoc(docRef).then((doc) => {
        if (doc.exists) {
            console.log("Document data:", doc.data());
            var url0 = doc.data().url;
            var name = doc.data().model;
            console.log('path: '+url0);
            const BUCKET_NAME = 'my-project-420-353715.appspot.com'
            var new_path = 'https://'+BUCKET_NAME+'.storage.googleapis.com/'+url0;
            console.log(new_path);
            const img = document.getElementById('image');
            img.setAttribute('src', new_path);
            document.getElementsByTagName('h1')[0].innerHTML = 'FAPP '+name;

        } else {
            // doc.data() will be undefined in this case
            console.log("No such document!");
        }
    }).catch((error) => {
        console.log("Error getting document:", error);
    });
}

const SIZE = 588663;
var BEST = [];
var BID = 0;
for (var i=0;i<1000;i++) {
    BEST.push(Math.floor(Math.random()*SIZE));
}

function next_best(step) {

    BID = (BID+step)%BEST.length;
    BID = BID < 0 ? BID + BEST.length : BID;
    console.log('BID', BID);
    new_image(BEST[BID]);

}

function set_best(new_best) {
    BEST = new_best;
    BID = 0;
    new_image(BEST[BID]);
}











// Initialize Firebase
const app = firebaseApp.initializeApp(firebaseConfig);
const storage = firebaseStorage.getStorage(app);
const db = firebaseFirestore.getFirestore(app);


onText((text) => {

    if (text.length > 1024) text = text.substring(0, 1024);


    firebaseFirestore.addDoc(firebaseFirestore.collection(db, "prompts"), {
        prompt: text,
      }).then((docRef) => {
        const id = docRef.id;
        console.log("Added to text database" + id + ': ' + text);
        var req = firebaseFirestore.doc(db, "clip_server", "request");

        firebaseFirestore.updateDoc(req, {
            "id": id
          }).then(()=>{
            console.log('Update requested');
            firebaseFirestore.onSnapshot(firebaseFirestore.doc(db, "clip_server", "response"), (doc) => {
                var data = doc.data();
                console.log("Current data: ", data);
                console.log("Current id: ", id);

                var news = String(id) in data;
                if (news) {
                    var best = data[String(id)];
                    console.log("Best: ", best);
                    set_best(best);
                }

            });
          });


      });
      



});


onFile((file) => {
    if (file.type == "image/jpeg" || file.type == "image/png") {
        var url = "uploads/"+file.name;
        var gurl = gname(url);
        const storageRef = firebaseStorage.ref(storage, "uploads/"+file.name);
        firebaseStorage.uploadBytes(storageRef, file).then((snapshot) => {
                    
            firebaseFirestore.addDoc(firebaseFirestore.collection(db, "prompts"), {
                url: gurl,
              }).then((docRef) => {
                const id = docRef.id;
                console.log("Added to text database" + id + ': ' + gurl);
                var req = firebaseFirestore.doc(db, "clip_server", "request");
        
                firebaseFirestore.updateDoc(req, {
                    "id": id
                  }).then(()=>{
                    console.log('Update requested');
                    firebaseFirestore.onSnapshot(firebaseFirestore.doc(db, "clip_server", "response"), (doc) => {
                        var data = doc.data();
                        console.log("Current data: ", data);
                        console.log("Current id: ", id);
        
                        var news = String(id) in data;
                        if (news) {
                            var best = data[String(id)];
                            console.log("Best: ", best);
                            set_best(best);
                        }
        
                    });
                  });
        
        
              });
        });
    }


});


// const viewRef = firebaseDatabase.ref(database, "view");
// firebaseDatabase.onValue(viewRef, (snapshot) => {
    
//     queueImage(snapshot.val());
//     // document.getElementById("view").setAttribute("src", snapshot.val());

// });


// document.getElementById("uploadButton").onclick = () => {

//     console.log("Click");
//     uploadFile((file) => {

//         console.log(file);

//         const storageRef = firebaseStorage.ref(storage, "uploads/"+file.name);
//         firebaseStorage.uploadBytes(storageRef, file).then((snapshot) => {
//             console.log("File uploaded!");
//         });

//     });


// }

const onUpd = () => {
    // const storageRef = refst(storage, "view/view.jpg");
    // getDownloadURL(storageRef).then((url) => {
    //     console.log("URL", url);
    //     document.getElementById("view").setAttribute("src", url+"?time="+Date.now());
    // });
}


// const viewRef = refdb(database, "update");
// onValuedb(viewRef, (snapshot) => {
//     console.log("update: ", snapshot.val());
//     onUpd();
// });


onLike(() => {
    

    firebaseFirestore.addDoc(firebaseFirestore.collection(db, "prompts"), {
        index: BEST[BID],
      }).then((docRef) => {
        const id = docRef.id;
        var req = firebaseFirestore.doc(db, "clip_server", "request");        

        firebaseFirestore.addDoc(firebaseFirestore.collection(db, "likes"), {
            index: BEST[BID],
            weight: 1
          })

        firebaseFirestore.updateDoc(req, {
            "id": id
          }).then(()=>{
            console.log('Update requested');
            firebaseFirestore.onSnapshot(firebaseFirestore.doc(db, "clip_server", "response"), (doc) => {
                var data = doc.data();
                console.log("Current data: ", data);
                console.log("Current id: ", id);

                var news = String(id) in data;
                if (news) {
                    var best = data[String(id)];
                    console.log("Best: ", best);
                    set_best(best);
                }

            });
          });


      });
      


})


// function getText(url){
//     // read text from URL location
//     var request = new XMLHttpRequest();
//     request.open('GET', url, true);
//     request.send(null);
//     request.onreadystatechange = function () {
//         if (request.readyState === 4 && request.status === 200) {
//             var type = request.getResponseHeader('Content-Type');
//             if (type.indexOf("text") !== 1) {
//                 return request.responseText;

//             }
//         }
//     }
// }


document.getElementById("image").addEventListener('click', (e) => {
    var seed = Math.floor(Math.random()*SIZE);
    console.log("SEED " + seed);
    var x = e.clientX;
    var dir = x>window.innerWidth/2?1:-1;
    next_best(dir);
}, true); 

new_image(BEST[BID]);