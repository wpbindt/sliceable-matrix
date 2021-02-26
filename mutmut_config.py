def pre_mutation(context):
    line = context.current_source_line.strip()
    if ' = TypeVar(' in line:
        context.skip = True

