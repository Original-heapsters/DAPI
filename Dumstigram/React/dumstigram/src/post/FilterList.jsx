import '../styles/FilterList.css';
import React, { useState, useEffect } from 'react';
import { Rings } from 'react-loader-spinner';
import 'bootstrap/dist/css/bootstrap.min.css';
import Accordion from 'react-bootstrap/Accordion';
import FilterItem from './FilterItem';
import * as api from '../api';

function FilterList() {
  const [isLoadingFilters, setIsLoadingFilters] = useState([false]);
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

  return (
    <div className="bg-light border">
      { isLoadingFilters
        ? <Rings color="#00BFFF" height={50} width={50} />
        : (
          <Accordion>
            <Accordion.Item eventKey="0">
              <Accordion.Header>Choose your filters</Accordion.Header>
              <Accordion.Body>
                {filters.map((filter) => (
                  <FilterItem key={filter.friendly_name} filter={filter} />
                ))}
              </Accordion.Body>
            </Accordion.Item>
          </Accordion>
        )}
    </div>
  );
}

export default FilterList;
