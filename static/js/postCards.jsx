function PostDetail(props) {
    return (
      <div className="post">
        <p> Post: {props.postText} </p>
        <p> Location: {props.lat} </p>
        <p> Date: {props.dateCreated} </p>
        <p> Tone Quality: {props.toneQuality} </p>
        <p> Hex Value: {props.hexValue} </p>
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
    const foo = document.createElement('div');

    for (const currentPost of posts) {
        postDetails.push(
            <PostDetail
                dateCreated={currentPost.dateCreated}
                lat={currentPost.lat}
                key={currentPost.postId}
                postText={currentPost.postText}
                toneQuality={currentPost.toneQuality}
                hexValue={currentPost.hexValue}
            />
        );
    }

    return <React.Fragment>{postDetails}</React.Fragment>;

}

ReactDOM.render(<PostDetailsContainer />, document.getElementById("all-posts"));