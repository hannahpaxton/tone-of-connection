function PostDetail(props) {
    return (
      <div className="post clearfix">
        <p><strong>Location:</strong> {props.location} </p>
        <p><strong>Date:</strong> {props.dateCreated} </p>
        <div><strong>Tone Qualities:</strong> {props.toneQualities.map(tone => 
          <div key={tone[2]}>
            <div style={{height:"20px", width:"20px", backgroundColor:tone[1], borderRadius: "100%", float: "left"}}></div>
            <div style={{display: "inline-block", paddingLeft:"20px"}}>{tone[0]}</div>
            <div style={{display: "inline-block", paddingLeft:"10px"}}>{tone[3] + "%"}</div>
          </div>
          ) } 
        </div>
        <p></p>
        <p><strong>I Asked:</strong> {props.postPrompt} </p>
        <p><strong>You Said:</strong> {props.postText} </p>
      </div>
    );
  }

function PostDetailsContainer() {
    const [posts, setPosts] = React.useState([]);
    const [hasError, setHasError] = React.useState(false);
 
    React.useEffect(() => {
      const fetchPosts = () => {
        fetch("/posts.json")
        .then((response) => response.json())
        .then((data) => {
          if (data.length === 0) {
            setHasError(true);
          }
          setPosts(data)});    
        };

      fetchPosts();
    }, []);

    const postDetails = [];

    for (const currentPost of posts) {
        postDetails.push(
            <PostDetail
                dateCreated={currentPost.dateCreated}
                location={currentPost.location}
                key={currentPost.postId}
                postText={currentPost.postText}
                postPrompt={currentPost.postPrompt}
                toneQualities={currentPost.toneQualities}
            />
        );
    }

    if (hasError) {
      return <p className="no_post">Looks like you haven't written anything yet. Go to <a href="/post">Create a Post</a> to fill up your journal!</p>
    }
    return <React.Fragment>{postDetails}</React.Fragment>;
    
}

ReactDOM.render(<PostDetailsContainer />, document.getElementById("all-posts"));