import { useState } from "react";
import axios from "axios";
import CodeMirror from "@uiw/react-codemirror";
import { okaidia } from "@uiw/codemirror-theme-okaidia";
import { javascript } from "@codemirror/lang-javascript";
import { Tab, Tabs, TabList, TabPanel } from "react-tabs";
import "react-tabs/style/react-tabs.css";

import "../index.css";

const Home = () => {
  const [entrada, setEntrada] = useState("");

  const [mensajes, setMensajes] = useState([]);
  const [errores, setErrores] = useState([]);
  const [simbolos, setSimbolos] = useState([]);
   const [vectores, setVectores] = useState([]); 

  const [activeTab, setActiveTab] = useState(0);
  const [imageSrc, setImageSrc] = useState("");

  const [zoom, setZoom] = useState(1);

  const handleWheel = (e) => {
    if (e.altKey) {
      e.preventDefault();
      // ajusta el factor de zoom (aquí +-0.1 por cada “tick” de rueda)
      const delta = -e.deltaY * 0.001;
      setZoom((z) => Math.min(3, Math.max(0.5, z + delta)));
    }
  };

  const handelTabSelect = (index) => {
    setActiveTab(index);
  };

  const readDocument = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        setEntrada(e.target.result);
      };
      reader.readAsText(file);
    }
  };

  const loadDatas = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(
        "http://localhost:5000/datas",
        entrada,
        { headers: { "Content-Type": "text/plain" } }
      );
      console.log("Respuesta del backend:", response.data);
      setMensajes(response.data.ListConsole);
      setErrores(response.data.ListError);
      setSimbolos(response.data.ListSymbol);
      setVectores(response.data.ListVector || []); 

      await loadImage();
    } catch {
      alert("Error al analizar la entrada. Por favor, revisa el formato.");
    }
  };

  const loadImage = async () => {
    try {
      const response = await axios.get("http://localhost:5000/ast", {
        responseType: "blob",
      });
      const blob = response.data;
      const imageUrl = URL.createObjectURL(blob);
      setImageSrc(imageUrl);
    } catch (err) {
      console.error("Error al cargar la imagen:", err);
    }
  };

  return (
    <div className="home-container">
      <div className="editor-section">
        <form onSubmit={loadDatas} className="control-form">
          <div className="buttons">
            <input
              type="file"
              id="fileInput"
              hidden
              onChange={readDocument}
            />
            <label htmlFor="fileInput" className="btn">
              Seleccionar archivo
            </label>
            <button type="submit" className="btn">
              Cargar
            </button>
          </div>
          <CodeMirror
            value={entrada}
            height="400px"
            width="900px"
            theme={okaidia}
            extensions={[javascript({ jsx: true })]}
            onChange={(value) => {
              setEntrada(value);
            }}
            className="editor"
          />
        </form>
      </div>

      <div className="tabs-section">
        <Tabs selectedIndex={activeTab} onSelect={handelTabSelect}>
          <TabList className="tab-list">
            <Tab>CONSOLA</Tab>
            <Tab>TABLA DE SÍMBOLOS</Tab>
            <Tab>ERRORES</Tab>
            <Tab>VECTORES</Tab>
            <Tab>AST</Tab>
          </TabList>

          <TabPanel className="tab-panel">
            <table className="striped-table">
              <thead>
                <tr>
                  <th>No</th>
                  <th>Mensaje</th>
                </tr>
              </thead>
              <tbody>
                {mensajes.map((m, index) => (
                  <tr key={index}>
                    <td>{index}</td>
                    <td>{m}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </TabPanel>

          <TabPanel className="tab-panel">
            <table className="striped-table">
              <thead>
                <tr>
                  <th>Símbolo</th>
                  <th>Tipo</th>
                  <th>Id</th>
                  <th>Valor</th>
                  <th>Parámetros</th>
                  <th>Ámbito</th>
                </tr>
              </thead>
              <tbody>
                {simbolos.map((simbolo, index) => (
                  <tr key={index}>
                    <td>{simbolo.simbolo}</td>
                    <td>{simbolo.tipo}</td>
                    <td>{simbolo.id}</td>
                    <td>{simbolo.valor}</td>
                    <td>{simbolo.parametros}</td>
                    <td>{simbolo.ambito}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </TabPanel>

          <TabPanel className="tab-panel">
            <table className="striped-table">
              <thead>
                <tr>
                  <th>Tipo</th>
                  <th>Descripción</th>
                  <th>Línea</th>
                  <th>Columna</th>
                </tr>
              </thead>
              <tbody>
                {errores.map((error, index) => (
                  <tr key={index}>
                    <td>{error.tipo}</td>
                    <td>{error.descripcion}</td>
                    <td>{error.linea}</td>
                    <td>{error.columna}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </TabPanel>
                
                <TabPanel className="tab-panel">
            <table className="striped-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Tipo</th>
                  <th>Dimensiones</th>
                  <th>Tamaño Total</th>
                  <th>Ámbito</th>
                  <th>Estrategia de Almacenamiento</th>
                  <th>Datos Lineales</th>
                </tr>
              </thead>
              <tbody>
                {vectores.map((vector, index) => (
                  <tr key={index}>
                    <td>{vector.id}</td>
                    <td>{vector.tipo}</td>
                    <td>{vector.dimensiones}</td>
                    <td>{vector.tamanio_total}</td>
                    <td>{vector.ambito}</td>
                    <td>
                      <pre style={{ 
                        fontSize: '12px', 
                        margin: 0, 
                        whiteSpace: 'pre-wrap',
                        maxWidth: '300px',
                        overflow: 'auto'
                      }}>
                        {vector.estrategia}
                      </pre>
                    </td>
                    <td>
                      <code style={{ 
                        fontSize: '12px',
                        maxWidth: '200px',
                        overflow: 'auto',
                        display: 'block'
                      }}>
                        {vector.datos}
                      </code>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </TabPanel>
          <TabPanel className="tab-panel">
            <div className="ast-image-container" onWheel={handleWheel}>
              {imageSrc && (
                <img
                  src={imageSrc}
                  alt="AST"
                  className="ast-image"
                  style={{ transform: `scale(${zoom})` }}
                />
              )}
            </div>
          </TabPanel>
        </Tabs>
      </div>
    </div>
  );
};

export default Home;