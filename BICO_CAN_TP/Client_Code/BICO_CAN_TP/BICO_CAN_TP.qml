import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.12
Window {
    id: window
    objectName: "window"
    width: 760
    height: 735

    visible: true
    title: qsTr("BICO CAN TP")
    // Signal transfer send data to Thread - begin ------------------------------------------------------------------
    signal toThread(string rev_mess, var rev_data)
    // Signal transfer send data to Thread - end ------------------------------------------------------------------
    // Handle data from Thread - begin ------------------------------------------------------------------
    signal fromThread(string rev_mess, var rev_data)
    onFromThread: function(rev_mess, rev_data)
    {
        // This block of code is allowed to be changed - begin -------------------
        if (rev_mess === "size")
        {
            button.height = rev_data.height
            button.width = rev_data.width
        }
        else if (rev_mess === "com_port_list")
        {
            console.log(rev_mess + " " + rev_data)
            availablePortsModel.clear()
            for (var i = 0; i < rev_data.length; i++) {
                availablePortsModel.append({"port": rev_data[i]});
            }
        }
        else if (rev_mess === "can_log")
        {
            console.log(rev_mess + " " + rev_data)
            canLogArea.text += rev_data + "\r\n"
            canLogArea.cursorPosition = canLogArea.text.length
        }
        // This block of code is allowed to be changed - end -------------------
    }
    // Handle data from Thread - end ------------------------------------------------------------------

    // Send data to Thread - begin ------------------------------------------------------------------
    Connections
    {
        target: window
//		onClosing: fromUI("terminate", "") // old syntax
        function onClosing (){ toThread("terminate", "") } // new syntax
    }
    // Send data to Thread - begin ------------------------------------------------------------------


//    Button {
//        objectName: "button"
//        id: button
//        x: 423
//        y: 287
//        text: qsTr("main")
//		onClicked:
//		{
//			var data_to_thread
//			if (qmess.text == "size")
//			{
//				// data_to_thread = Qt.size(int(qdata.text), int(qdata.text))
//				data_to_thread = Qt.size(Number(qdata.text), Number(qdata.text))
//			}
//			else
//			{
//				data_to_thread = qdata.text
//			}
//			toThread(qmess.text, data_to_thread)
//		}
//    }
//    TextField {
//        id: qmess
//        x: 205
//        y: 149
//        width: 318
//        height: 40
//        placeholderText: qsTr("mess")
//    }
//    TextField {
//        id: qdata
//        x: 205
//        y: 214
//        width: 318
//        height: 40
//        placeholderText: qsTr("data")
//    }

    ComboBox {
        id: comPortDropdown
        x: 538
        y: 446
        width: 107
        height: 40
        model: availablePortsModel
        font.pixelSize: 15
        anchors.verticalCenterOffset: 196
        anchors.horizontalCenterOffset: 220
        background: Rectangle {
            border.color: "gray"  // Set border color
            border.width: 1       // Set border width
            radius: 5              // Set corner radius (optional)
        }

        onActivated: {
            console.log("Selected COM port: " + comPortDropdown.currentText)
        }
        onPressedChanged: {
            if (!pressed)
            {
                toThread("com_port_list_update", "")
            }
        }
    }

    // Button to connect to the device
    Button {
        id: connectButton
        x: 656
        y: 446
        text: "Connect"
        width: 88
        height: 40
        font.pixelSize: 15
        background: Rectangle {
            border.color: "gray"  // Set border color
            border.width: 1       // Set border width
            color: "lightgray"
            radius: 5              // Set corner radius (optional)
        }
        onClicked: {
            // Connect to CAN device logic goes here
            // console.log("Connecting with baudrate: " + baudrateField.text)
            var txid = txID.text
            var rxid = rxID.text
            if (txid === "")
            {
                txid = txID.placeholderText
            }
            if (rxid === "")
            {
                rxid = rxID.placeholderText
            }
            toThread(this.text, `{"serial_port": "${comPortDropdown.currentText}", "can_baudrate": ${baudrateField.text}, "rxid": "${rxid}", "txid": "${txid}"}`)
            if (comPortDropdown.currentText != "")
            {
                if (this.text == "Connect")
                {
                    this.text = "Disconnect"
                }
                else if (this.text == "Disconnect")
                {
                    this.text = "Connect"
                }
            }
        }
    }


    // Wide area to monitor CAN frames
    Item {
        x: 14
        y: 60
        width: 735
        height: 350
        ScrollView {
            id: scrollView
            anchors.fill: parent
            TextArea {
                id: canLogArea
                 placeholderText: "CAN log appear here...."
                readOnly: false
                font.pixelSize: 15
                font.family: "Consolas" // Replace with your desired font
                // Add a border and background color
                background: Rectangle {
                    border.color: "black"  // Set border color
                    border.width: 1        // Set border width
                    radius: 5              // Set corner radius (optional)
                }
            }
        }
    }
    // Input field for CAN ID
    TextField {
        id: rxID
        x: 15
        y: 446
        width: 137
        height: 40
        placeholderText: "18DAF110x"
        font.pixelSize: 15
        background: Rectangle {
            border.color: "gray"  // Set border color
            border.width: 1       // Set border width
            radius: 5              // Set corner radius (optional)
        }
    }

    Text {
        x: 158
        y: 424
        text: "Target ID"
        font.pixelSize: 15
    }

    TextField {
        id: txID
        x: 158
        y: 446
        width: 137
        height: 40
        font.pixelSize: 15
        background: Rectangle {
            radius: 5
            border.color: "#808080"
            border.width: 1
        }
        placeholderText: "18DA10F1x"
    }


    // Input field for CAN baudrate
    Text {
        x: 449
        y: 424
        text: "CAN Baud:"
        font.pixelSize: 15
    }
    TextField {
        id: baudrateField
        x: 449
        y: 446
        width: 77
        height: 40
        // placeholderText: text // Syncing placeholderText with the text value
        text: "500000"                      // Initial value
        enabled: false
        font.pixelSize: 15
        background: Rectangle {
            border.color: "gray"  // Set border color
            border.width: 1       // Set border width
            radius: 5              // Set corner radius (optional)
        }
    }


    Text {
        x: 15
        y: 424
        text: "Source ID"
        font.pixelSize: 15
    }
    Text {
        x: 538
        y: 424
        text: "Serial Port:"
        font.pixelSize: 15
    }

    // Input field for CAN data
    TextField {
        id: canDataField
        x: 14
        y: 501
        width: 631
        height: 40
        placeholderText: "10 01"
        font.pixelSize: 15
        background: Rectangle {
            border.color: "gray"  // Set border color
            border.width: 1       // Set border width
            radius: 5              // Set corner radius (optional)
        }
        onTextChanged: {
            text = text.toUpperCase()
        }
    }    // Button to send CAN frame
    Button {
        id: sendButton
        x: 656
        y: 501
        text: "Send"
        width: 88
        height: 40
        font.pixelSize: 15
        background: Rectangle {
            border.color: "gray"  // Set border color
            border.width: 1       // Set border width
            color: "lightgray"
            radius: 5              // Set corner radius (optional)
        }
        onClicked: {
            // Logic to send CAN frame goes here
            // console.log("Sending CAN frame with ID: " + txID.text + " and Data: " + canDataField.text)
            var can_id = txID.text
            var can_data = canDataField.text
            if (can_id === "")
            {
                can_id = txID.placeholderText
            }
            if (can_data === "")
            {
                can_data = canDataField.placeholderText
            }
            toThread(text, `{"can_id": "${can_id}", "can_data": "${can_data}"}`)
        }
    }

    // ListModel to hold the COM port data
    ListModel {
        id: availablePortsModel
    }

    Text {
        x: 20
        y: 38
        text: "Date-Time"
        font.pixelSize: 15
    }

    Text {
        x: 252
        y: 38
        text: "ID"
        font.pixelSize: 15
    }

    Text {
        x: 334
        y: 38
        text: "DLC/[idx]"
        font.pixelSize: 15
    }

    Text {
        id: byte0
        x: 420
        y: 38
        text: "[0]"
        font.pixelSize: 15
    }

    Text {
        id: byte1
        x: byte0.x + 40
        y: 38
        text: "[1]"
        font.pixelSize: 15
    }

    Text {
        id: byte2
        x: byte0.x + 40*2
        y: 38
        text: "[2]"
        font.pixelSize: 15
    }

    Text {
        id: byte3
        x: byte0.x + 40*3
        y: 38
        text: "[3]"
        font.pixelSize: 15
    }

    Text {
        id: byte4
        x: byte0.x + 40*4
        y: 38
        text: "[4]"
        font.pixelSize: 15
    }

    Text {
        id: byte5
        x: byte0.x + 40*5
        y: 38
        text: "[5]"
        font.pixelSize: 15
    }

    Text {
        id: byte6
        x: byte0.x + 40*6
        y: 38
        text: "[6]"
        font.pixelSize: 15
    }

    Text {
        id: byte7
        x: byte0.x + 40*7
        y: 38
        text: "[7]"
        font.pixelSize: 15
    }
    TextField {
        id: canDataField1
        x: 15
        y: 547
        width: 631
        height: 40
        font.pixelSize: 15
        placeholderText: "10 01"
        background: Rectangle {
            radius: 5
            border.color: "#808080"
            border.width: 1
        }
        onTextChanged: {
            text = text.toUpperCase()
        }
    }

    Button {
        id: sendButton1
        x: 657
        y: 547
        width: 88
        height: 40
        text: "Send"
        font.pixelSize: 15
        background: Rectangle {
            color: "#d3d3d3"
            radius: 5
            border.color: "#808080"
            border.width: 1
        }
        onClicked: {
                // Logic to send CAN frame goes here
            // console.log("Sending CAN frame with ID: " + txID.text + " and Data: " + canDataField.text)
            var can_id = txID.text
            var can_data = canDataField1.text
            if (can_id === "")
            {
                can_id = txID.placeholderText
            }
            if (can_data === "")
            {
                can_data = canDataField1.placeholderText
            }
            toThread(text, `{"can_id": "${can_id}", "can_data": "${can_data}"}`)
        }
    }

    TextField {
        id: canDataField2
        x: 14
        y: 593
        width: 631
        height: 40
        font.pixelSize: 15
        placeholderText: "10 01"
        background: Rectangle {
            radius: 5
            border.color: "#808080"
            border.width: 1
        }
        onTextChanged: {
            text = text.toUpperCase()
        }
    }

    Button {
        id: sendButton2
        x: 656
        y: 593
        width: 88
        height: 40
        text: "Send"
        font.pixelSize: 15
        background: Rectangle {
            color: "#d3d3d3"
            radius: 5
            border.color: "#808080"
            border.width: 1
        }
        onClicked: {
                // Logic to send CAN frame goes here
            // console.log("Sending CAN frame with ID: " + txID.text + " and Data: " + canDataField.text)
            var can_id = txID.text
            var can_data = canDataField2.text
            if (can_id === "")
            {
                can_id = txID.placeholderText
            }
            if (can_data === "")
            {
                can_data = canDataField2.placeholderText
            }
            toThread(text, `{"can_id": "${can_id}", "can_data": "${can_data}"}`)
        }
    }


    TextField {
        id: canDataField3
        x: 14
        y: 639
        width: 631
        height: 40
        font.pixelSize: 15
        placeholderText: "10 01"
        background: Rectangle {
            radius: 5
            border.color: "#808080"
            border.width: 1
        }
        onTextChanged: {
            text = text.toUpperCase()
        }
    }


    Button {
        id: sendButton3
        x: 656
        y: 639
        width: 88
        height: 40
        text: "Send"
        font.pixelSize: 15
        background: Rectangle {
            color: "#d3d3d3"
            radius: 5
            border.color: "#808080"
            border.width: 1
        }
        onClicked: {
                // Logic to send CAN frame goes here
            // console.log("Sending CAN frame with ID: " + txID.text + " and Data: " + canDataField.text)
            var can_id = txID.text
            var can_data = canDataField3.text
            if (can_id === "")
            {
                can_id = txID.placeholderText
            }
            if (can_data === "")
            {
                can_data = canDataField3.placeholderText
            }
            toThread(text, `{"can_id": "${can_id}", "can_data": "${can_data}"}`)
        }
    }

    TextField {
        id: canDataField4
        x: 14
        y: 685
        width: 631
        height: 40
        font.pixelSize: 15
        placeholderText: "10 01"
        background: Rectangle {
            radius: 5
            border.color: "#808080"
            border.width: 1
        }
        onTextChanged: {
                text = text.toUpperCase()
            }
    }


    Button {
        id: sendButton4
        x: 656
        y: 685
        width: 88
        height: 40
        text: "Send"
        font.pixelSize: 15
        background: Rectangle {
            color: "#d3d3d3"
            radius: 5
            border.color: "#808080"
            border.width: 1
        }
        onClicked: {
                // Logic to send CAN frame goes here
                // console.log("Sending CAN frame with ID: " + txID.text + " and Data: " + canDataField.text)
                var can_id = txID.text
                var can_data = canDataField4.text
            if (can_id === "")
            {
                can_id = txID.placeholderText
            }
            if (can_data === "")
            {
                can_data = canDataField4.placeholderText
            }
            toThread(text, `{"can_id": "${can_id}", "can_data": "${can_data}"}`)
        }
    }


    // Define tab order here
    Component.onCompleted: {
        canDataField.focus = true
        // canDataField.Tab.focusChain = sendButton
        // sendButton.Tab.focusChain = canDataField1
    }
}
/*##^##
Designer {
    D{i:0;formeditorZoom:1.1}
}
##^##*/
