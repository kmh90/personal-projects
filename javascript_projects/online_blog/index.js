import express from "express";
import bodyParser from "body-parser";

const app = express();
const port = 3000;
const options = {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    timeZone: 'Asia/Singapore' // GMT+8
};

var postList = [];

class BlogPost {
    constructor(title, msg) {
        this.title = title;
        this.msg = msg;
        this.initialDate = new Date(2020, 0, 1).toLocaleDateString('en-US', options);
        this.lastUpdatedDate = "";
    }
    updatePost(newTitle, message) {
        this.title = newTitle;
        this.msg = message;
        this.lastUpdatedDate = new Date().toLocaleDateString('en-US', options);
        // return { "message" : this.msg, "lastUpdatedDate" : this.lastUpdatedDate};
    }
}

app.use(express.static("public"));

app.use(bodyParser.urlencoded({ extended: true }));

app.get("/", (req, res) => {
    console.log(typeof(postList[0]));
    res.render("index.ejs", {
        posts: postList
    });
});

app.get("/faqs", (req, res) => {
    res.render("faq.ejs", {
        posts: postList
    });
});

app.get("/gfaqs", (req, res) => {
    res.render("gfaq.ejs", {
        posts: postList
    });
});

app.post("/create", (req, res) => {
    console.log(req.body);
    var userPost = new BlogPost(req.body["title"], req.body["message"]);
    console.log(userPost);
    postList.push(userPost);
    res.redirect("/");
});

app.post("/edit", (req, res) => {
    // console.log(req.body);
    var postNumberToUpdate = parseInt(req.body["postNumber"]);

    res.render("edit.ejs", {
        postNumber: postNumberToUpdate,
        posts: postList
    });
});

app.post("/save", (req, res) => {
    // console.log(req.body);
    var postNumberToUpdate = parseInt(req.body["postNumber"]);
    var newTitle = req.body["title"];
    var newPost = req.body["message"];
    // console.log(postList[postNumberToUpdate])
    var blogPost = postList[postNumberToUpdate]
    blogPost.updatePost(newTitle, newPost);

    // Re-arrange BlogPost object to last item in the list
    postList.splice(postNumberToUpdate, 1);
    postList.push(blogPost);

    res.redirect("/");
});

app.post("/delete", (req, res) => {
    var postNumberToUpdate = parseInt(req.body["postNumber"]);
    var tmpList = [];

    for (let k = 0; k < postList.length; k++) {
        if (k !== postNumberToUpdate) {
            tmpList.push(postList[k]);
        }
    };
    postList = tmpList;
    res.redirect("/");
});

app.listen(port, () => {
    console.log(`Listening on port ${port}`);
});