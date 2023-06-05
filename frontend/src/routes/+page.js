/** @type {import('./$types').PageLoad} */
export async function load() {
    try {
      const response = await fetch('http://127.0.0.1:8000/');
      const data = await response.json();
      return {
        students: data.content, // Assuming the response contains a "content" property with the list of students
      };
    } catch (error) {
      console.error('Error loading data:', error);
      return {
        error: 'Failed to fetch data',
      };
    }
  }
  