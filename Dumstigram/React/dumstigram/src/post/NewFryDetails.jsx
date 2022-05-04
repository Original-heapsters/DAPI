import '../styles/NewFryDetails.css';
import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import Stack from 'react-bootstrap/Stack';
import Form from 'react-bootstrap/Form';
import FloatingLabel from 'react-bootstrap/FloatingLabel';
import FilterList from './FilterList';

function NewFryDetails({
  setCaption,
  setExpiration,
}) {
  const handleCaptionChange = (event) => {
    const fieldVal = event.target.value;
    setCaption(fieldVal);
  };

  const handleExpirationChange = (event) => {
    const fieldVal = event.target.value;
    setExpiration(fieldVal);
  };

  return (
    <div>
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
            defaultValue="43200"
          >
            <option id="timeXShort" value="30">30 seconds</option>
            <option id="timeShort" value="3600">1 hour</option>
            <option id="timeLong" value="43200">12 hours</option>
            <option id="timeXLong" value="86400">1 day</option>
          </Form.Select>
        </FloatingLabel>
      </Stack>
      <FilterList />
    </div>
  );
}

export default NewFryDetails;
