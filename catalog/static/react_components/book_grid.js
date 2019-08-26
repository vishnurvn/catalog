class BookList extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            data: null
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
                    data: data
                })
            }
        )
    }

    componentWillMount() {
        this.getData(1)
    }

    render() {
        if (this.state.data == null) {
            return (
                <div id="spinner-wrapper" className="display-spinner">
                    <div className="spinner-border text-success" id="loading-spinner" role="status">
                        <span className="sr-only">Loading...</span>
                    </div>
                </div>
            )
        }
        let pagination = this.state.data.num_pages.map((item) => {
            return (
                <li className="page-item page-numbers">
                    <button className="page-link" onClick={() => this.getData(item+1)} value={item+1}>{item+1}</button>
                </li>
            )
        });
        let results = this.state.data.book_data.map((item) => {
            return (
                <div className="card mb-3">
                    <div className="row no-gutters">
                        <div className="col-md-4">
                            <img src="/static/media/cover.jpg" className="card-img book-pic" alt="..."/>
                        </div>
                        <div className="col-md-8">
                            <div className="card-body">
                                <h5 className="card-title">{item.title}</h5>
                                <p className="card-text">by: <span>{item.author}</span></p>
                                <p className="card-text">This is a wider card with supporting text below as a natural lead-in to additional content. This content is a little bit longer.</p>
                                <a href={`http://127.0.0.1:5000/book/${item.id}`} className="btn btn-primary">Button</a>
                                <p className="card-text"><small className="text-muted">Last updated 3 mins ago</small></p>
                            </div>
                        </div>
                    </div>
                </div>
            )
        })
        return (
            <div>
                {results}
                <nav aria-label="Page navigation example">
                    <ul className="pagination justify-content-center">
                        <li className="page-item"><a className="page-link" href="#">Previous</a></li>
                        {pagination}
                        <li className="page-item"><a className="page-link" href="#">Next</a></li>
                    </ul>
                </nav>
            </div>
        )
    }
}

let domContainer = document.getElementById('book-grid-container')
ReactDOM.render(<BookList/>, domContainer)