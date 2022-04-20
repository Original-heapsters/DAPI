import '../styles/CreateNewFryForm.css';
import React, { useState, useEffect } from 'react';
import { Rings } from 'react-loader-spinner';
import 'bootstrap/dist/css/bootstrap.min.css';
import Modal from 'react-bootstrap/Modal';
import Stack from 'react-bootstrap/Stack';
import Form from 'react-bootstrap/Form';
import Card from 'react-bootstrap/Card';
import Accordion from 'react-bootstrap/Accordion';
import FloatingLabel from 'react-bootstrap/FloatingLabel';
import * as api from '../api';

function CreateNewFryForm({
  setSelectedFile,
  setCaption,
  setExpiration,
}) {
  const [isLoadingFilters, setIsLoadingFilters] = useState([false]);
  const [selectedFileUrl, setSelectedFileUrl] = useState('https://www.generationsforpeace.org/wp-content/uploads/2018/03/empty.jpg');
  const [filters, setFilters] = useState();

  useEffect(() => {
    setIsLoadingFilters(true);
    async function getFilters() {
      const possibleFilters = await api.getFilters();
      return possibleFilters;
    }
    getFilters()
      .then((possFilters) => {
        setFilters(possFilters);
        setIsLoadingFilters(false);
      })
      .catch(() => {
        setIsLoadingFilters(false);
      });
  }, []);

  const changeHandler = (event) => {
    const tmppath = URL.createObjectURL(event.target.files[0]);
    setSelectedFileUrl(tmppath);
    setSelectedFile(event.target.files[0]);
  };

  const handleCaptionChange = (event) => {
    const fieldVal = event.target.value;
    setCaption(fieldVal);
  };

  const handleExpirationChange = (event) => {
    const fieldVal = event.target.value;
    setExpiration(fieldVal);
  };

  return (
    <Modal.Body>
      <Stack gap={3}>
        <div className="createPost__preview">
          <img
            className="createPost__image"
            src={selectedFileUrl}
            alt=""
          />
          <input type="file" name="file" onChange={changeHandler} />
        </div>
        <Stack direction="horizontal" gap={2}>
          <FloatingLabel className="me-auto" controlId="captionInput" label="Caption">
            <Form.Control
              className="me-auto"
              as="textarea"
              placeholder="I cant believe how fried this meme got"
              onChange={handleCaptionChange}
              style={{ height: '100px', width: '60vw' }}
            />
          </FloatingLabel>
          <FloatingLabel controlId="floatingSelect" label="Set expiration time">
            <Form.Select
              aria-label="Default select example"
              style={{ width: '20vw' }}
              onChange={handleExpirationChange}
            >
              <option id="timeXShort" value="30">30 seconds</option>
              <option id="timeShort" value="3600">1 hour</option>
              <option id="timeLong" value="43200" selected>12 hours</option>
              <option id="timeXLong" value="86400">1 day</option>
            </Form.Select>
          </FloatingLabel>
        </Stack>
        <div className="bg-light border">
          { isLoadingFilters
            ? <Rings color="#00BFFF" height={50} width={50} />
            : (
              <Accordion>
                <Accordion.Item eventKey="0">
                  <Accordion.Header>Choose your filters</Accordion.Header>
                  <Accordion.Body>
                    {filters.map((filter) => (
                      <div key={filter.id} className="createPost__form__radio">
                        <Form.Check type="checkbox" id={filter.id} name="selected_filter" value={filter.id} label={filter.id} />
                        <Card style={{ width: '18rem' }}>
                          <Card.Img variant="top" src={filter.example_url} />
                          <Card.Body>
                            <Card.Title>{filter.friendly_name}</Card.Title>
                            <Card.Text>
                              {filter.description}
                            </Card.Text>
                          </Card.Body>
                        </Card>
                      </div>
                    ))}
                  </Accordion.Body>
                </Accordion.Item>
              </Accordion>
            )}
        </div>
      </Stack>
    </Modal.Body>
  );
}

export default CreateNewFryForm;
