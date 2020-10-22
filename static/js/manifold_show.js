///////////// 结果的展示


 num=0;
setInterval(function () {
    num=(num+1)%5;
    console.log(num);
    $.getJSON('/heatmap/'+num, null, function (dataval) {


    var data = [
        {
            z: dataval,
            type: 'contour'

        }
    ];

    Plotly.plot('heatmap', data,{smoothing:true});

})

},10000);

/**
 * Created by chenking on 2018/3/22.
 */

//////////////////////热力图


$.getJSON('/evalresult', null, function (dataval) {

       


    var data = [
        {
            x: dataval.x,
            y: dataval.y,
            type: 'scatter'
        }
    ];
    var layout = {
        size:[-100,50,0,50,100],
        width: 800,
        height: 500,
        margin: {
            l: 50,
            r: 50,
            b: 100,
            t: 100,
            pad: 4
        },
        smoothing:true,
        paper_bgcolor: '#0000000',
        plot_bgcolor: '#0000000'
    };
    TESTER = document.getElementById('resultshow');
    Plotly.newPlot(TESTER, data, layout);



})


////////////// 网络拓扑图

function renderobj(type, x, y, z, nodetype) {
    if (type == 1 || type == 2 || type == 4 || type == 6)   var geo = new THREE.BoxGeometry(x, y, z);
    else if (type == 3) var geo = new THREE.CylinderGeometry(x, y, z);
    else if (type == 5) var geo = new THREE.BoxGeometry(x, y, z);
    var metrail = new THREE.MeshLambertMaterial({map: THREE.ImageUtils.loadTexture(nodetype["" + type].imgurl)});
    return new THREE.Mesh(geo, metrail);
}
function initscene(nodetype) {
    // Setup scene
    const scene = new THREE.Scene();
    scene.add(Graph);
    scene.add(new THREE.AmbientLight(colortable.white));


    Graph.nodeThreeObject(function (node) {


        if (node.type == 1 || node.type == 2) {
            return renderobj(node.type, 20, 20, 20, nodetype);//圆柱

        } else if (node.type == 3) {
            return renderobj(node.type, 10, 10, 20, nodetype);
        } else if (node.type == 4) {
            return renderobj(node.type, 20, 20, 20, nodetype);
        } else if (node.type == 5) {
            return renderobj(node.type, 20, 20, 20, nodetype);
        } else if (node.type == 6) {
            return renderobj(node.type, 20, 20, 20, nodetype);
        }


    });

    // Setup camera
    const camera = new THREE.PerspectiveCamera();
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    camera.lookAt(Graph.position);
    camera.position.z = 200;
    camera.position.x = 80;
    camera.position.y = 50;

    // Add camera controls
    const tbControls = new TrackballControls(camera, renderer.domElement);
    // Kick-off renderer
    (function animate() { // IIFE
        Graph.tickFrame();
        // Frame cycle
        tbControls.update();
        renderer.render(scene, camera);
        requestAnimationFrame(animate);
    })();
}
// Gen random data
const N = 300;


const colortable = {'green': 0x00ff00, 'red': 0xffff00, 'blue': 0x0000ff, 'yellow': 0xcfb53b, 'white': 0xffffff};
const Graph = new ThreeForceGraph()
    .linkColor(colortable.red)
    .linkWidth(3)
    .jsonUrl('/nodesmap')

    .numDimensions(3);


// Setup renderer
const renderer = new THREE.WebGLRenderer();

renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setClearColor(0xffffff, 0);
document.getElementById('topology').appendChild(renderer.domElement);


$.ajax({
    url: '/nodetype',
    complete: function (response) {

        console.log(response.responseJSON);

        initscene(response.responseJSON);
    }
});


//////////////////