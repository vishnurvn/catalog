class BookList extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            bookData: null
        }
    }
    getData = (page) => {
        const url = 'http://127.0.0.1:5000/get_book_list'
        let data = {
            'page': page
        }
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        }).then(
            response => {
                return response.json()
            }
        ).then(
            data => {
                this.setState({
                    bookData: data
                })
            }
        )
    }
    componentWillMount() {
        this.getData(1)
    }
    render() {
        if (this.state.bookData == null) {
            return (
                <div id="spinner-wrapper" className="display-spinner">
                    <div className="spinner-border text-success" id="loading-spinner" role="status">
                        <span className="sr-only">Loading...</span>
                    </div>
                </div>
            )
        }
        let results = this.state.bookData.map((item) => {
            return (
                <div className="card w-75">
                    <div className="card-body">
                        <h5 className="card-title">{item.title}</h5>
                        <p className="card-text">by: <span>{item.author}</span></p>
                        <a href={`http://127.0.0.1:5000/book/${item.id}`} className="btn btn-primary">Button</a>
                    </div>
                </div>
            )
        })
        return (
            <div>
                {results}
            </div>
        )
    }
}

let domContainer = document.getElementById('book-grid-container')
ReactDOM.render(<BookList/>, domContainer)