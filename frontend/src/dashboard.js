import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

const Dashboard = () => {
  const [classes, setClasses] = useState([]);

  useEffect(() => {
    // fetch class information
    axios.get('/api/classes')
      .then(response => setClasses(response.data))
      .catch(error => console.log(error));
  }, []);

  const handleAddInstructor = (classId) => {
    // add instructor to class
    axios.post(`/api/classes/${classId}/instructors`)
      .then(response => {
        // update classes state with new instructor information
        const updatedClasses = classes.map(classInfo => {
          if (classInfo.id === classId) {
            return {
              ...classInfo,
              instructors: [...classInfo.instructors, response.data]
            };
          } else {
            return classInfo;
          }
        });
        setClasses(updatedClasses);
      })
      .catch(error => console.log(error));
  };

  return (
    <div>
      <header>
        <h1>OurHour</h1>
        <nav>
          <ul>
            <li><Link to="/login">Sign Out</Link></li>
          </ul>
        </nav>
      </header>
      <main>
      <div className="dashboard">
      {classes.length > 0 ? (
        classes.map((c) => (
          <Link to={`/class/${c.id}`} key={c.id}>
            <div className="class-card">
              <h2>{c.name}</h2>
              <p>Queue length: {c.queue.length}</p>
              <button>Add instructor</button>
            </div>
          </Link>
        ))
      ) : (
        <div className="no-classes">
          <div className="message-card">
            <h1>No classes found</h1>
          </div>
        </div>
      )}
    </div>
    </main>
    </div> 
  );
}

export default Dashboard;


