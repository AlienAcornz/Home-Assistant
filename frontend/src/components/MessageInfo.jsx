function MessageInfo({ message }) {
    return (
        <tr className="message-info">
            <td>{message.message}</td>
            <td>{message.time}</td>
            <td>{message.tag}</td>
        </tr>
    )
}

export default MessageInfo