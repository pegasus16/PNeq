const config = {
    type: Phaser.AUTO,
    width: 400,
    height: 720,
    parent:'phaser',
    backgroundColor: '#f4f4f4',
    scene: {
        preload: preload,
        create: create,
        update: update
    }

};
const nodewidth=50;

const nodeheight=30;

let nodes = [];
let draggedNode = null;
let offsetX = 0;
let offsetY = 0;
let startX = 0;
let startY = 0;

function preload() {
    this.load.image('node', 'images/node.png');  // Placeholder image for nodes
    this.load.image('node2', 'images/node2.png');  // Placeholder image for nodes
}

function create() {
    // window.updateHtmlElement('Game has started!');
    this.add.text(100, 200, "电路1", {
        fontSize: '24px',
        color: '#000000',
        fontFamily: 'Microsoft YaHei, sans-serif'
    }).setOrigin(0.5);
    this.add.text(300, 200, "电路2", {
        fontSize: '24px',
        color: '#000000',
        fontFamily: 'Microsoft YaHei, sans-serif'
    }).setOrigin(0.5);

    this.add.text(200, 30, "简介", {
        fontSize: '32px',
        color: '#000000',
        fontFamily: 'Microsoft YaHei, sans-serif'
    }).setOrigin(0.5);

    this.add.text(200, 100, "拖动输出端按钮以调整布尔电路。\n假设某一对应关系1->7代表\n当输入001是输出111", {
        fontSize: '20px',
        color: '#000000',
        fontFamily: 'Microsoft YaHei, sans-serif'
    }).setOrigin(0.5);
    // Create 8 rows and 2 columns of nodes
    for (let i = 0; i < 8; i++) {
        for (let j = 0; j < 4; j++) {
            const x = (2*j+1) * nodewidth;  // x position for each column
            const y = i * (nodeheight+5)+250;   // y position for each row

            // const node = this.add.image(x, y, 'node').setInteractive();
            // node.setData('index', { row: i, col: j });

            const number = i;  // Generate a number for the node

            const node = this.add.container(x, y);

            // Draw a rectangle (frame) for the node
            const graphics = this.add.graphics();
            graphics.lineStyle(2, 0x000000, 1);  // Set border color and thickness
            graphics.strokeRect(-nodewidth/2, -nodeheight/2, nodewidth, nodeheight);  
            let image = this.add.image(0, 0, 'node');
            image.alpha=0.5;

            // Create a text object inside the rectangle
            const text = this.add.text(0, 0, number, {
                fontSize: '18px',
                color: '#000000',
                fontFamily: 'Arial'
            }).setOrigin(0.5);
            node.setDepth(0);
            // let bounds=Phaser.Geom.Rectangle(-nodewidth/2, -nodeheight/2, nodewidth, nodeheight);
            node.add([image,text , graphics]);
            node.setSize(nodewidth, nodeheight);  // Set the size of the container

            // const node=text;

            node.setInteractive();  // Only make the rectangle interactive

            node.setData('index', { row: i, col: j });
            node.setData('position', { x: x, y: y });

            console.info(node.getBounds());

            // Only make nodes in the second column draggable
            if (j === 1 || j===3) {
                this.add.text(x-nodewidth+2, y-2, "->", {
                    fontSize: '24px',
                    color: '#000000',
                    fontFamily: 'Microsoft YaHei, sans-serif'
                }).setOrigin(0.5);
                node.on('pointerdown', (pointer) => {
                    console.info("pointerdown");
                    node.setDepth(-10);
                    draggedNode = node;
                    startX = node.x;
                    startY = node.y;
                    offsetX = pointer.x - node.x;
                    offsetY = pointer.y - node.y;
                });

                node.on('pointermove', (pointer) => {
                    if (draggedNode) {
                        // console.info("pointermove",draggedNode);
                        draggedNode.x = pointer.x;
                        draggedNode.y = pointer.y;
                    }
                });

                node.on('pointerup', (pointer) => {
                    console.info("pointerup");
                    if (draggedNode) {
                        // Check if the node is close enough to swap
                        const otherNode = getNodeUnderPointer(pointer,draggedNode.getData('index').row,draggedNode.getData('index').col);
                        console.info("otherNode ",otherNode );
                        console.info("otherNode exist",otherNode !== null);
                        console.info("otherNode not equal draggedNode",otherNode !== draggedNode);
                        // console.info("otherNode in col 1",otherNode.getData('index').col === 1);
                        console.info("if",otherNode !== null && otherNode !== draggedNode);
                        if (otherNode && otherNode !== draggedNode) {
                            
                            console.info("swap");
                            console.info("otherNode in col 1",otherNode.getData('index').col === 1);
                            swapNodes(draggedNode, otherNode);
                            draggedNode.setDepth(0);
                            
                        }
                        else
                        {
                            console.info("re");
                            draggedNode.setPosition(draggedNode.getData('position').x,draggedNode.getData('position').y);
                            draggedNode.setDepth(0);

                        }
                        startX=0;
                        startY=0;
                        draggedNode = null;
                    }
                });
            }

            nodes.push(node);
        }
    }

    const confirm1 = this.add.container(200, 580);
    const graphics1 = this.add.graphics();
    graphics1.lineStyle(2, 0x000000, 1);  // Set border color and thickness
    graphics1.strokeRect(-nodewidth*3.5, -nodeheight/2, nodewidth*7, nodeheight);  
    let image1 = this.add.image(0, 0, 'node2');
    image1.alpha=0.5;

    // Create a text object inside the rectangle
    const text1 = this.add.text(0, 0, "查询两电路是否为输入N等价", {
        fontSize: '22px',
        color: '#000000',
        fontFamily: 'Arial'
    }).setOrigin(0.5);
    // let bounds=Phaser.Geom.Rectangle(-nodewidth/2, -nodeheight/2, nodewidth, nodeheight);
    confirm1.add([image1, text1 , graphics1]);
    confirm1.setSize(nodewidth*7, nodeheight);
    confirm1.setInteractive();
    confirm1.on('pointerdown', (pointer) => 
    {
        console.info("confirm1");
        post(0);
    });

    const confirm2 = this.add.container(200, 640);
    const graphics2 = this.add.graphics();
    graphics2.lineStyle(2, 0x000000, 1);  // Set border color and thickness
    graphics2.strokeRect(-nodewidth*3.5, -nodeheight/2, nodewidth*7, nodeheight);  
    let image2 = this.add.image(0, 0, 'node2');
    image2.alpha=0.5;

    // Create a text object inside the rectangle
    const text2 = this.add.text(0, 0, "查询两电路是否为输出P等价", {

        fontSize: '22px',
        color: '#000000',
        fontFamily: 'Arial'
    }).setOrigin(0.5);
    confirm2.add([image2,text2 , graphics2]);
    // confirm2.add([text2 , graphics2]);

    confirm2.setSize(nodewidth*7, nodeheight);
    confirm2.setInteractive();

    confirm2.on('pointerdown', (pointer) => 
    {
        console.info("confirm2");
        // post(1);
    });
}


function post(type)
{
    let p1 = [];
    let p2 = [];
    for (let i = 0; i < 32; i++) 
        {
            if(nodes[i].getData("index").col===1)p1.push(nodes[i].getData("index").row);
            if(nodes[i].getData("index").col===3)p2.push(nodes[i].getData("index").row);
            
        }
    console.info("post",p1,p2);
    window.get_result(type,p1,p2);

}
function update() {
    // Any real-time updates can go here
}

function getNodeUnderPointer(pointer,row,col) {
    // Check if any node is under the pointer
    // console.info(nodes[3].getBounds(),pointer.x, pointer.y);
    // console.info(nodes[3].getBounds().contains(pointer.x, pointer.y));
    console.info(nodes.find(node => node.getBounds().contains(pointer.x, pointer.y)));

    for (let i = 0; i < 32; i++) 
    {
        if(nodes[i].getBounds().contains(pointer.x, pointer.y))
        {
            if(nodes[i].getData("index").row!==row&&nodes[i].getData("index").col===col)return nodes[i];
        }
    }

    return null;
}

function swapNodes(node1, node2) {
    // const tempX = startX;
    // const tempY = startY;

    // Swap positions
    node1.setPosition(node2.getData('position').x, node2.getData('position').y);
    node2.setPosition(node1.getData('position').x, node1.getData('position').y);

    node1.setData('position',{x : node1.x , y : node1.y});
    node2.setData('position',{x : node2.x , y : node2.y});

    // Swap data indices
    const tempIndex = node1.getData('index');
    node1.setData('index', node2.getData('index'));
    node2.setData('index', tempIndex);
}

const game = new Phaser.Game(config);