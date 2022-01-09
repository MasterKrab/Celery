const esbuild = require("esbuild")
const {watch} = require("chokidar")

const files = ["js/books.js", "js/scripts.js"]

const isDev = process.env.NODE_ENV === 'development'

const options = {
    entryPoints: files,
    bundle: true,
    minify: true,
    outdir: "static/js",
}

const build = () => {
    esbuild.build(options)
        .catch(console.error)
}

build();

if (isDev) {
    const watcher = watch(["js/**/*"]);
    watcher.on("change", build);
}
