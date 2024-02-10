import clang.cindex


def get_functions(version):
    index = clang.cindex.Index.create()
    tu = index.parse(f"wasmpy_build/include/{version}/Python.h")

    functions = []

    for child in tu.cursor.get_children():
        if not child.location.file.name.startswith(f"wasmpy_build/include/{version}"):
            # exclude external files
            continue

        if child.kind == clang.cindex.CursorKind.FUNCTION_DECL:
            if clang.cindex.conf.lib.clang_Cursor_isFunctionInlined(child):
                # inline function
                continue

            func_result = child.type.get_result().spelling
            func_name = child.spelling
            func_args = []

            # get arguments
            for arg in child.get_arguments():
                arg_name = arg.spelling
                arg_type = arg.type.spelling
                func_args.append((arg_type, arg_name))

            functions.append((func_result, func_name, func_args))

    return functions
