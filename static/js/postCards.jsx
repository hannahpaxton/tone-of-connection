function PostDetail(props) {
    return (
      <div className="post">
        <p> Post: {props.postText} </p>
        <p> Location: {props.lat} </p>
        <p> Date: {props.dateCreated} </p>
        <div> Tone Qualities: {props.toneQualities.map(tone => 
          <div key={tone[2]}>
            <div style={{height:"20px", width:"20px", backgroundColor:tone[1], float: "left"}}></div>
            <div style={{paddingLeft:"30px"}}>{tone[0]}</div>
          </div>
          ) } 
        </div>
      </div>
    );
  }
  
function PostDetailsContainer() {
    const [posts, setPosts] = React.useState([]);

    React.useEffect(() => {
      const fetchPosts = () => {
        fetch("/posts.json")
        .then((response) => response.json())
        .then((data) => {
          setPosts(data)});      
      };

      fetchPosts();
    }, []);

    const postDetails = [];

    for (const currentPost of posts) {
        postDetails.push(
            <PostDetail
                dateCreated={currentPost.dateCreated}
                lat={currentPost.lat}
                key={currentPost.postId}
                postText={currentPost.postText}
                toneQualities={currentPost.toneQualities}
            />
        );
    }

    return <React.Fragment>{postDetails}</React.Fragment>;

}

ReactDOM.render(<PostDetailsContainer />, document.getElementById("all-posts"));