class TableGrid extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            data: null
        }
    }

    getData = (page) => {
        const url = `http://127.0.0.1:5000/admin/${this.props.item}/${page}`
        fetch(url, {
            'method': 'GET',
            'headers': {
                'Content-Type': 'application/json'
            }
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

    sayMeh() {
        console.log('Say meh')
    }

    componentDidMount() {
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
        } else {
            let headers_keys = []
            for (let key in this.state.data[0]) {
                headers_keys.push(key)
            }

            let headers = headers_keys.map(item => {
                return (
                    <th>{item}</th>
                )
            })

            let results = this.state.data.map(item => {
                return (
                    <tr>
                        <td>
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox"/>
                            </div>
                        </td>
                        {Object.keys(item).map(key => {
                            return (<td>{item[key]}</td>)
                        })}
                    </tr>
                )
            })
            return (
                <table className="table">
                    <thead>
                        <tr>
                            <th></th>
                            {headers}
                        </tr>
                    </thead>
                    <tbody>
                        {results}
                    </tbody>
                </table>
            )
        }
    }
}

let domContainerUsers = document.getElementById('user')
ReactDOM.render(<TableGrid item="users"/>, domContainerUsers)

let domContainerBooks = document.getElementById('books')
ReactDOM.render(<TableGrid item="books"/>, domContainerBooks)
