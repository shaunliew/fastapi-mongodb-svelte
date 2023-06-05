<script>
    /** @type {import('./$types').PageData} */
    export let data;
    let students = data.students;
</script>

<div class = "m-10">
    {#if students.length > 0}
        {#each students as student}
            <div class="block card card-hover p-4 m-4 max-w-sm variant-filled-surface">
                <header class="card-header">Name: <div class = "badge variant-filled-primary"> {student.name}</div></header>
                <section class="p-1 pl-4">
                    Email: <div class = "badge variant-filled-secondary"> {student.email} </div>
                    <br/>

                </section>
                <section class="p-1 pl-4">
                    Course: <div class = "badge variant-filled-error"> {student.course}</div>
                    <br/>
                </section>
                <section class="p-1 pl-4">
                    GPA: <div class = "badge variant-filled-warning"> {student.gpa}</div>
                </section>
                <footer class="card-footer"></footer>
            </div>
        {/each} 
    {:else}
        <p>No data</p>
    {/if}
</div>